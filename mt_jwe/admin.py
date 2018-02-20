from django.contrib import admin

from . import models
from .utils import keys_utils


@admin.register(models.SitecodeJWEKeys)
class SitecodeJWEKeysAdmin(admin.ModelAdmin):
    list_display = ['sitecode', 'date_created']
    readonly_fields = ('in_keys_json', 'date_created')

    def save_model(self, request, obj, form, change):
        if not obj.in_keys_json:
            obj.in_keys_json.update(keys_utils.generate_rsa_keypair())
            obj.in_keys_json.update(keys_utils.generate_oct_key())
        super().save_model(request, obj, form, change)
