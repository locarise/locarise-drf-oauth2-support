from django.test import Client
from django.test import TestCase
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class TestConfig(TestCase):
    client_class = Client

    def test_auth(self):
        url = reverse('rest_framework:token')

        payload = {
            'scope': 'read write',
            'client_id': None,
            'client_secret': None,
            'email': 'john@example.com',
            'password': 'john_password',
        }

        res = self.client.post(url, data=payload, format='json')
        self.assertEqual(res.status_code, 400)
