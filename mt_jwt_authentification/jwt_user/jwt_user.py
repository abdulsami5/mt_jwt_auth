from datetime import timedelta, datetime
import unicodedata
from django.contrib.auth.models import AnonymousUser


class JWTPermissionsMixin:
    is_superuser = False
    groups = []
    user_permissions = []

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through their
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        return permissions

    def get_all_permissions(self, obj=None):
        """
        user.get_group_permissions + user.get_user_permissions
        """
        permissions = set()
        return permissions

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return False


class JWTUser(JWTPermissionsMixin, AnonymousUser):
    # from AbstractBaseUser --------------------------------

    def __init__(self, payload):
        super().__init__()
        self.username = payload.get('username', '')
        self.uuid = payload.get('uuid', '')
        self._groups = payload.get('groups', list())
        self.groups = self._groups

        self.is_active = True if datetime.utcnow() < datetime.fromtimestamp(payload.get('exp', datetime.utcnow().timestamp())) else False

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @classmethod
    def get_email_field_name(cls):
        return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if username else username

    # from AbstractUser --------------------------------
    username = ''
    first_name = ''
    last_name = ''
    email = ''
    is_staff = False
    is_active = True
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']


    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        # send_mail(subject, message, from_email, [self.email], **kwargs)
        pass

    @property
    def is_staff(self):
        return "STAFF" in str(self.groups)

    @property
    def is_admin(self):
        return "ADMIN" in self.groups

    @property
    def is_designer(self):
        return "DESIGNER" in self.groups
