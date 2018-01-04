import json
import random

from datetime import datetime

from django.conf import settings
from django.core.cache import caches

CACHE_CONFIG_NAME = 'session' if 'session' in settings.CACHES.keys() else next(iter(settings.CACHES.keys()))


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    return ''.join(random.choice(allowed_chars) for i in range(length))


def generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(length=50, allowed_chars=chars)


class JSONSerializer(object):
    """
    Simple wrapper around json to be used in signing.dumps and
    signing.loads.
    """

    def dumps(self, obj):
        return json.dumps(obj, separators=(',', ':')).encode('latin-1')

    def loads(self, data):
        return json.loads(data.decode('latin-1'))


class SuspiciousSession(Exception):
    """The session may be tampered with"""
    pass


class RedisCommonStorage(object):
    cache = caches[CACHE_CONFIG_NAME]
    serializer = JSONSerializer()

    def __init__(self, prefix='redis-common-storage'):
        self.prefix = prefix

    def get_or_create(self, key, exp):
        value = self.get_obj(key)
        if value:
            return key, value
        else:
            value = {'secret_key': generate_secret_key()}
            self.set_obj(key, value, exp)
            return key, value

    def get_obj(self, key):
        if type(key) == bytes:
            key = key.decode("utf-8")
        full_key = '{}.{}'.format(self.prefix, key)
        value_str = self.cache.get(full_key)
        if value_str:
            return self.serializer.loads(value_str)
        else:
            return None

    def set_obj(self, key, obj, exp):
        full_key = '{}.{}'.format(self.prefix, key)
        value_str = self.serializer.dumps(obj)
        timeout = int((exp - datetime.utcnow()).total_seconds()) if isinstance(exp, datetime) else 30000
        self.cache.set(key=full_key, value=value_str, timeout=timeout)
        # print(self.cache.keys('*')[0] if hasattr(self.cache, 'keys') else 'hasn\'t keys')
        # print(self.get_obj(2))
