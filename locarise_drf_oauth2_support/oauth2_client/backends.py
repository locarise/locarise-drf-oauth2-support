# -*- coding: utf-8 -*-

"""
Locarise OAuth2 backend, docs at:
    https://accounts.locarise.com
"""

from social_core.backends.oauth import BaseOAuth2


class LocariseOAuth2(BaseOAuth2):
    """
    Locarise OAuth authentication backend
    """
    name = 'locarise-oauth2'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]
    ID_KEY = 'uid'
    DEFAULT_SCOPE = ['read']

    def authorization_url(self):
        return self.setting(
            'AUTHORIZATION_URL',
            'https://accounts.locarise.com/oauth2/authorize'
        )

    def access_token_url(self):
        return self.setting(
            'TOKEN_URL',
            'https://accounts.locarise.com/oauth2/access_token'
        )

    def get_user_details(self, response):
        """
        Return user details from Locarise Account server
        """
        return {
            'email': response['email'],
            'uid': response['uid'],
            'first_name': response.get('first_name'),
            'last_name': response.get('last_name'),
            'is_staff': response.get('is_staff'),
            'is_active': response.get('is_active'),
            'is_superuser': response.get('is_superuser'),
            'locale': response.get('locale'),
            'organizations': response.get('organizations', []),
        }

    def api_profile_url(self):
        return self.setting(
            'API_PROFILE_URL',
            'https://accounts.locarise.com/userinfo.json'
        )

    def user_data(self, access_token, *args, **kwargs):
        """
        Loads user data from service
        """
        data = self.get_json(
            self.api_profile_url(),
            headers={'Authorization': 'Bearer {}'.format(access_token)}
        )
        return data
