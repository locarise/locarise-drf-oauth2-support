from __future__ import unicode_literals

from django.test import TestCase

from locarise_drf_oauth2_support.users.factories import UserF
from locarise_drf_oauth2_support.users.models import User


class TestModels(TestCase):

    def test_user(self):

        user = UserF()
        self.assertTrue(isinstance(user, User))
        self.assertTrue(user.check_password('pass'))

        user.save()

        self.assertEqual(
            user.get_full_name(),
            '{} {}'.format(user.first_name, user.last_name)
        )
        self.assertEqual(user.get_short_name(), user.first_name)

        self.assertRaises(ValueError, User.objects.create_user, None)

    def test_user_organizations(self):
        user = UserF()

        data = {}
        user.organizations = data
        user.save()
        self.assertEqual(user.organizations, data)

        data = [
            {
                'uid': 'orga-uid',
                'name': 'orga-name',
                'role': 'manager'
            }
        ]
        user.organizations = data
        user.save()
        self.assertEqual(user.organizations, data)
