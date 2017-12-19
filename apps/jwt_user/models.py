import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='User public identifier')

