# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django_extensions.db.fields import (
    ModificationDateTimeField,
    CreationDateTimeField
)

from locarise.utils import sane_repr


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.pop('username', None)

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            uid=extra_fields.get('uid'),
            email=UserManager.normalize_email(email),
            first_name=extra_fields.get('first_name') or '',
            last_name=extra_fields.get('last_name') or '',
            is_staff=extra_fields.get('is_staff') or False,
            is_active=extra_fields.get('is_active') or True,
            is_superuser=extra_fields.get('is_superuser') or False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Users within the Django authentication system are represented by this model.
    """
    # Fields from SAMS
    uid = models.CharField(
        primary_key=True, max_length=22, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    locale = models.CharField(max_length=5)

    # Local fields
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    objects = UserManager()

    USERNAME_FIELD = 'email'

    __repr__ = sane_repr('email', 'uid')

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name
