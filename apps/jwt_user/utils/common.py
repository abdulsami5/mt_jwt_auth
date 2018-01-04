
import jwt
from django.utils.translation import ugettext as _

from django.conf import settings
from django.utils.encoding import smart_text

from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions

from apps.jwt_user.storages.django_cache import RedisCommonStorage
from apps.jwt_user.utils.jwt_wraper import JWTAuthDec


def get_jwt_value(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()

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
    try:
        payload = JWTAuthDec(keys_storage=storage).validate_payload(token)
    except jwt.ExpiredSignature:
        msg = _('Signature has expired.')
        raise exceptions.AuthenticationFailed(msg)
    except jwt.DecodeError:
        msg = _('Error decoding signature.')
        raise exceptions.AuthenticationFailed(msg)
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed()
    return payload
