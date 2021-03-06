# Generated by Django 2.0.2 on 2018-02-19 14:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SitecodeJWEKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitecode', models.SlugField(unique=True)),
                ('description', models.CharField(max_length=1024)),
                ('domain', models.CharField(blank=True, default='', max_length=128)),
                ('in_keys_json', django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='rsa_private, rsa_public, symmetric')),
                ('out_keys_json', django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='rsa_public, symmetric')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['sitecode'],
            },
        ),
    ]
