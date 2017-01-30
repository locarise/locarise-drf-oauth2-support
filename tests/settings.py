from __future__ import unicode_literals, absolute_import

import os

DEBUG = True
USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'social_django',
    'locarise_drf_oauth2_support.users',
    'locarise_drf_oauth2_support.oauth2_client',
]

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'locarise_drf_oauth2_support.oauth2_client.backends.LocariseOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOCARISE_OAUTH2_KEY = os.environ.get(
    'LOCARISE_OAUTH2_CLIENT_ID',
    '299a50da2f9605c0c643'  # client url: http://127.0.0.1:8000
)
SOCIAL_AUTH_LOCARISE_OAUTH2_SECRET = os.environ.get(
    'LOCARISE_OAUTH2_CLIENT_SECRET',
    '907f6b89795ccfc093b678b85226f2c88e25a4d0'
)

LOCARISE_API_PROFILE = '127.0.0.1:8001/userinfo.json'
LOCARISE_OAUTH2_AUTHORIZATION_URL = '127.0.0.1:8001/oauth2/authorize'
LOCARISE_OAUTH2_TOKEN_URL = '127.0.0.1:8001/oauth2/access_token'

SOCIAL_AUTH_USER_FIELDS = [
    'uid', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'locale'
]

AUTH_USER_MODEL = 'users.User'

SECRET_KEY = '6p%gef2(6kvjsgl*7!51a7z8c3=u4uc&6ulpua0g1^&sthiifp'
