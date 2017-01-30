from django.test import TestCase

from locarise_drf_oauth2_support.users.factories import UserF
from locarise_drf_oauth2_support.users.models import User


class TestModels(TestCase):

    def test_user(self):

        user = UserF()
        self.assertTrue(isinstance(user, User))

        user.save()
