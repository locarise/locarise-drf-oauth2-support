# Locarise Django Rest-Framework Oauth2 Support

This module provides

* a `python-social-auth` and `oauth2` support for django-rest-framework,
connected to `Locarise Oauth2 provider`.
* an `users` application (models and DRF views)

Install this lib if you need to add login to Locarise Auth provider
(`accounts.locarise.com`)

Works only with `Django >= 1.7` and `djangorestframework>=3.0.1`

## Installation

Install with pip:
```
pip install -e git+https://github.com/locarise/locarise-drf-oauth2-support#egg=locarise-drf-oauth2-support
```

You have the choice to install only the Oauth client, only the users
application or both.

### Oauth2 Client Installation

#### Requirements

A user models with at least:
* `uid`: 22 characters CharField
* `email` EmailField

If you haven't it yet, you can install the users app (see below).

A Oauth2 client:
* `url` likes `http://127.0.0.1:8009/`
* `redirect uri` likes `http://127.0.0.1:8009/complete/locarise/`
* `client type` is `confidential`

You can create a client or read its parameters through
https://accounts.locarise.com/admin/provider/client/ interface.

#### Installation

Add these apps to your INSTALLED_APPS

```
INSTALLED_APPS = (
    ...
    'social.apps.django_app.default',
    'locarise_drf_oauth2_support.oauth2-client',
)
```

Add these context processors to your TEMPLATE_CONTEXT_PROCESSORS

```
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    }
]
```

Add Locarise authentication backend:
```
AUTHENTICATION_BACKENDS = (
    'locarise_drf_oauth2_support.oauth2_client.backends.LocariseOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
```

Configure your client ID and Secret
```
SOCIAL_AUTH_LOCARISE_KEY = os.environ.get(
    'LOCARISE_OAUTH2_CLIENT_ID',
    'XXXXXXXXXXXXXXXXXXXXX'
)
SOCIAL_AUTH_LOCARISE_SECRET = os.environ.get(
    'LOCARISE_OAUTH2_CLIENT_SECRET',
    'YYYYYYYYYYYYYYYYYYYYY'
)
```

Optional (Locarise production endpoints are set by default)

```
SOCIAL_AUTH_LOCARISE_TOKEN_URL = os.environ.get(
    'LOCARISE_OAUTH2_TOKEN_URL',
    'http://127.0.0.1:8001/oauth2/access_token'
)
SOCIAL_AUTH_LOCARISE_AUTHORIZATION_URL = os.environ.get(
    'LOCARISE_OAUTH2_AUTHORIZATION_URL',
    'http://127.0.0.1:8001/oauth2/authorize'
)
SOCIAL_AUTH_API_PROFILE_URL = os.environ.get(
    'LOCARISE_API_PROFILE_URL',
    'http://127.0.0.1:8001/userinfo.json'
)
```

According to your `User` model fields, you have to define which fields from
`accounts.locarise.com` you want to copy in local (choices come from
http://accounts.locarise.com/userinfo endpoint).
```
SOCIAL_AUTH_USER_FIELDS = [
    'uid', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'locale'
]
```

Include auth urls to your urls.py

```
urlpatterns = patterns(
    ...
    # Authentication
    url(r'', include('locarise_drf_oauth2_support.oauth2_client.urls')),
)
```

#### Notes

If you want your API has the same behavior than the others, add these apps
to your INSTALLED_APPS

```
INSTALLED_APPS = (
    ...
    'corsheaders',
    'rest_framework.authtoken',
)
```

Set up REST Framework classes:

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

### Users application installation

Add this app to your INSTALLED_APPS

```
INSTALLED_APPS = (
    ...
   'locarise_drf_oauth2_support.users',
)
```

And declare:

```
AUTH_USER_MODEL = 'users.User'
```

Then include auth urls to your urls.py

```
urlpatterns = patterns(
    ...
    # Users
    url(r'', include('locarise_drf_oauth2_support.users.urls')),
)
```




