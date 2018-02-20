from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from rest_framework import authentication, exceptions

from mt_jwt_auth.jwt_user.utils.common import get_jwt_value, jwt_decode_handler


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
        token = get_jwt_value(request)
        if token is None:
            return None

        payload = jwt_decode_handler(token)

        user = self.authenticate_credentials(payload)

        return user, token

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
        return '{0} realm="{1}"'.format(settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)

