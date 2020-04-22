# -*- coding: utf-8 -*-

from shortuuidfield import ShortUUIDField

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django_extensions.db.fields import ModificationDateTimeField, CreationDateTimeField
from simple_history.models import HistoricalRecords

try:
    from django.contrib.postgres.fields import JSONField
except ImportError:  # pragma: no cover
    from jsonfield import JSONField


from .utils import sane_repr


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, uid=None, **extra_fields):

        extra_fields.pop("username", None)

        if not email:
            raise ValueError("Users must have an email address")

        if uid:
            user, _ = self.model.objects.get_or_create(uid=uid)
        else:
            user, _ = self.model.objects.get_or_create(email=email)

        user.email = email

        for field, value in extra_fields.items():
            setattr(user, field, value)

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Users within the Django authentication system are represented by
    this model.
    """

    # Fields from SAMS
    uid = ShortUUIDField(primary_key=True, editable=False)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    locale = models.CharField(max_length=5)
    organizations = JSONField(null=True)

    # Local fields
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    objects = UserManager()

    USERNAME_FIELD = "email"

    history = HistoricalRecords()

    __repr__ = sane_repr("email",)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name
