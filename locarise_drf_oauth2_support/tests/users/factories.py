# -*- coding: utf-8 -*-
import factory

from django.utils import timezone

from locarise_drf_oauth2_support.users.models import User


class UserF(factory.DjangoModelFactory):
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    password = 'sha1$caffc$30d78063d8f2a5725f60bae2aca64e48804272c3'
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = timezone.utc.localize(timezone.datetime(2000, 1, 1))
    password = factory.PostGenerationMethodCall('set_password', 'pass')

    class Meta:
        model = User
