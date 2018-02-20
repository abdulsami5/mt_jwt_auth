from django.db import models
from django.contrib.postgres.fields import JSONField


class SitecodeJWEKeys(models.Model):
    sitecode = models.SlugField(unique=True)
    description = models.CharField(max_length=1024)
    domain = models.CharField(max_length=128, blank=True, default='')
    in_keys_json = JSONField(help_text='rsa_private, rsa_public, symmetric', default=dict)
    out_keys_json = JSONField(help_text='rsa_public, symmetric', default=dict)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sitecode']

    def __str__(self):
        return self.sitecode
