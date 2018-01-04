from rest_framework import permissions

from apps.jwt_user.utils.common import jwt_decode_handler, get_jwt_value


class JWTBasePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        token = get_jwt_value(request)
        if token is None:
            return False
        else:
            # TODO: check payload ? how ?
            payload = jwt_decode_handler(token)
            return True

    def has_object_permission(self, request, view, obj):
        return True


class AnyGroupJWTBasePermission(JWTBasePermission):

    '''
        give access for all authenticated users that belong to any group
    '''

    def has_permission(self, request, view):
        # TODO Temp. Remove as deprecated when all apps use jwt authentication
        old_perm = False

        try:
            # For old jwt token parsing logic
            old_perm = (super().has_permission(request, view) and
                        request.jwt_payload.get('uuid') and
                        request.jwt_payload.get('groups'))
        except:
            # Just go to check the new permission
            pass

        return old_perm or (request.user.is_authenticated and request.groups)