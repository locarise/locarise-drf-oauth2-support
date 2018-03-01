from __future__ import unicode_literals

import json
import mock

from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from locarise_drf_oauth2_support.users.factories import UserF

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


User = get_user_model()


class TestOauth2ClientViewsTestCase(TestCase):
    client_class = Client

    def test_obtain_auth_token(self):
        url = reverse('rest_framework:token')

        # 1. Bad requests
        payload = {
            'email': 'john@example.com',
        }
        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 400)

        payload = {
            'email': 'john@example.com',
            'password': 'john_password',
        }
        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 400)

        # 2. It works
        user = UserF()
        payload = {
            'email': user.email,
            'password': 'pass',
        }
        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 200)

        # 3. User is inactive
        user = UserF(is_active=False)
        payload = {
            'email': user.email,
            'password': 'pass',
        }
        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 400)

    @mock.patch('locarise_drf_oauth2_support.oauth2_client.backends.LocariseOAuth2.get_json')  # noqa
    def test_oauth_obtain_auth_token(self, get_json):

        # 1. bad requests
        url = reverse('rest_framework:oauth2-token', kwargs={
            'backend_name': 'unknown'
        })
        payload = {
            'email': 'john@example.com',
            'access_token': 'john_access_token'
        }
        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 404)

        # Wrong access_token
        get_json.return_value = {}

        url = reverse('rest_framework:oauth2-token', kwargs={
            'backend_name': 'locarise-oauth2'
        })
        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 403)

        payload = {
            'access_token': 'john_access_token'
        }
        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 400)

        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 400)

        # 2. It works

        self.assertEqual(User.objects.count(), 0)

        get_json.return_value = {
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'uid': 'john-uid',
            'is_staff': True,
            'is_active': True,
            'is_superuser': False,
            'locale': 'en-us',
            'organizations': [
                {
                    'uid': 'orga-uid',
                    'name': 'orga-name',
                    'role': 'manager'
                }
            ]
        }

        payload = {
            'email': 'john@example.com',
            'access_token': 'john_access_token'
        }

        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 200)
        try:
            data = res.json()
        except AttributeError:
            data = json.loads(res.content)
        self.assertIn('token', data)

        self.assertEqual(User.objects.count(), 1)

        john = User.objects.all().first()

        self.assertEqual(john.email, 'john@example.com')
        self.assertEqual(john.first_name, 'John')
        self.assertEqual(john.last_name, 'Doe')
        self.assertEqual(john.uid, 'john-uid')
        self.assertEqual(john.is_staff, True)
        self.assertEqual(john.is_active, True)
        self.assertEqual(john.is_superuser, False)
        self.assertEqual(john.locale, 'en-us')
        self.assertEqual(
            john.organizations,
            [
                {
                    'uid': 'orga-uid',
                    'name': 'orga-name',
                    'role': 'manager'
                }
            ]
        )

    @mock.patch('locarise_drf_oauth2_support.oauth2_client.backends.LocariseOAuth2.get_json')  # noqa
    def test_oauth_obtain_auth_token_user_is_not_active(self, get_json):

        url = reverse('rest_framework:oauth2-token', kwargs={
            'backend_name': 'locarise-oauth2'
        })

        payload = {
            'email': 'john@example.com',
            'access_token': 'john_access_token'
        }

        get_json.return_value = {
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'uid': 'john-uid',
            'is_staff': False,
            'is_active': False,
            'is_superuser': False,
            'locale': 'en-us',
            'organizations': [
                {
                    'uid': 'orga-uid',
                    'name': 'orga-name',
                    'role': 'manager'
                }
            ]
        }

        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 400)


class UserViewsTestCaseTestCase(TestCase):

    def test_current_user_view(self):

        client = Client()
        url = reverse('me')

        res = client.get(url)
        self.assertEqual(res.status_code, 401)  # It shouldn't be a 403.

        user = UserF()
        client.login(email=user.email, password='pass', format='json')
        res = client.get(url)

        self.assertEqual(res.status_code, 200)
        try:
            data = res.json()
        except AttributeError:
            data = json.loads(res.content)
        self.assertEqual(data['first_name'], user.first_name)
