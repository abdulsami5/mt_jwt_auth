from django.utils.translation import ugettext as _

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


JWT_ALGORITHM = 'HS256'


class PasswordField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = {'input_type': 'password'}
        else:
            kwargs['style']['input_type'] = 'password'
        super(PasswordField, self).__init__(*args, **kwargs)


class JSONWebTokenSerializer(serializers.Serializer):
    @property
    def object(self):
        return self.validated_data
    """
    Serializer class used to validate a username and password.
    'username' is identified by the custom UserModel.USERNAME_FIELD.
    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return getattr(get_user_model(), 'USERNAME_FIELD', 'username')

    def validate(self, data):
        credentials = {
            self.username_field: data.get(self.username_field),
            'password': data.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                return {
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
