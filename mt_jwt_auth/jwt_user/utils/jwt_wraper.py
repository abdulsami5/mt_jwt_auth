import jwt


class JWTAuthDec(object):
    keys_storage = dict()
    algorithms = 'HS256'

    def __init__(self, keys_storage=None):
        if keys_storage:
            self.keys_storage = keys_storage

    def create_token(self, payload, key=None):
        _key, value = self.keys_storage.get_or_create(key, payload['exp'])
        secret_key = value.get('secret_key')
        payload['key'] = _key
        return jwt.encode(payload=payload, key=secret_key, algorithm=self.algorithms)

    def validate_payload(self, token):
        payload = self.get_payload(token)
        key, value = self.keys_storage.get_or_create(payload.get('key', None), payload.get('exp'))
        secret_key = value.get('secret_key')
        return self.get_payload(token, secret_key=secret_key, verify=True)

    def get_payload(self, token, secret_key='', verify=False):
        return jwt.decode(jwt=token, key=secret_key, algorithms=self.algorithms, verify=verify)
