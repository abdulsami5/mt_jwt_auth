import jwt
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _

from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header

from apps.jwt_user.storages.django_cache import RedisCommonStorage
from apps.jwt_user.utils.jwt_wraper import JWTAuthDec

JWT_AUTH_HEADER_PREFIX = 'JWT'


def get_jwt_value(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = JWT_AUTH_HEADER_PREFIX.lower()

    if not auth:
        #     if api_settings.JWT_AUTH_COOKIE:
        #         return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
        return None

    if smart_text(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        msg = _('Invalid Authorization header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = _('Invalid Authorization header. Credentials string '
                'should not contain spaces.')
        raise exceptions.AuthenticationFailed(msg)

    return auth[1]


def jwt_decode_handler(token):
    storage = RedisCommonStorage()
    payload = JWTAuthDec(keys_storage=storage).validate_payload(token)
    return payload


class ObtainJWTCustomAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class BaseJSONWebTokenAuthentication(authentication.BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return user, jwt_value

    @staticmethod
    def authenticate_credentials(payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        uuid = payload.get('uuid')

        if not uuid:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `JWT_AUTH_HEADER_PREFIX`. For example:

        Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """
    www_authenticate_realm = 'api'

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)

