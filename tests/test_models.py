from __future__ import unicode_literals

from django.test import TestCase

from locarise_drf_oauth2_support.users.factories import UserF, AdminUserF
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

        admin = AdminUserF()
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_user(self):

        email = 'john@doe.com'
        password = 'pass'

        fields = {
            'first_name': 'first_name_v1',
            'last_name': 'last_name_v1',
            'is_staff': False,
            'is_active': False,
            'is_superuser': False,
            'locale': 'loc_1',
            'organizations': ['organizations_v1'],
        }

        # 1. Create an new user

        self.assertEqual(User.objects.count(), 0)

        user = User.objects.create_user(email, password, **fields)
        self.assertEqual(User.objects.count(), 1)
        db_user = User.objects.first()
        self.assertEqual(db_user.uid, user.uid)
        self.assertEqual(db_user.email, email)
        self.assertEqual(db_user.first_name, fields['first_name'])
        self.assertEqual(db_user.last_name, fields['last_name'])
        self.assertEqual(db_user.is_staff, fields['is_staff'])
        self.assertEqual(db_user.is_active, fields['is_active'])
        self.assertEqual(db_user.is_superuser, fields['is_superuser'])
        self.assertEqual(db_user.locale, fields['locale'])
        self.assertEqual(db_user.organizations, fields['organizations'])

        # 2. Try to create the user again with his email

        user = User.objects.create_user(email, password)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().uid, user.uid)
        self.assertEqual(User.objects.first().email, email)

        # 3. Try to create the user again but with his uid

        user = User.objects.create_user('john2@doe.com', password, uid=user.uid)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().uid, user.uid)
        self.assertEqual(User.objects.first().email, 'john2@doe.com')

        # 4. Update the user fields

        fields_v2 = {
            'first_name': 'first_name_v2',
            'last_name': 'last_name_v2',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True,
            'locale': 'loc_2',
            'organizations': ['organizations_v2'],
        }

        user = User.objects.create_user(
            'john3@doe.com', password, uid=user.uid, **fields_v2
        )
        self.assertEqual(User.objects.count(), 1)
        db_user = User.objects.first()
        self.assertEqual(User.objects.first().uid, user.uid)
        self.assertEqual(User.objects.first().email, 'john3@doe.com')
        self.assertEqual(db_user.first_name, fields_v2['first_name'])
        self.assertEqual(db_user.last_name, fields_v2['last_name'])
        self.assertEqual(db_user.is_staff, fields_v2['is_staff'])
        self.assertEqual(db_user.is_active, fields_v2['is_active'])
        self.assertEqual(db_user.is_superuser, fields_v2['is_superuser'])
        self.assertEqual(db_user.locale, fields_v2['locale'])
        self.assertEqual(db_user.organizations, fields_v2['organizations'])

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
