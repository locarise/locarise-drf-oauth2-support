from __future__ import unicode_literals

from django.test import TestCase

from locarise_drf_oauth2_support.oauth2_client.backends import LocariseOAuth2


class TestBackendTestCase(TestCase):

    def test_methods(self):

        backend = LocariseOAuth2(strategy=None)

        self.assertEqual(
            backend.authorization_url(),
            'https://accounts.locarise.com/oauth2/authorize'
        )
        self.assertEqual(
            backend.access_token_url(),
            'https://accounts.locarise.com/oauth2/access_token'
        )
        self.assertEqual(
            backend.api_profile_url(),
            'https://accounts.locarise.com/userinfo.json'
        )

        details = backend.get_user_details(response={'email': '', 'uid': ''})
        self.assertListEqual(
            sorted(details.keys()),
            sorted(
                [
                    'email', 'uid', 'first_name', 'last_name', 'is_staff',
                    'is_active', 'is_superuser', 'locale', 'organization_set'
                ]
            )
        )
