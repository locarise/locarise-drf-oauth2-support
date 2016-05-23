# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib.auth.views import logout, login



from .views import ObtainAuthToken, OAuthObtainAuthToken


login_args = {'template_name': 'oauth2_client/login.html'}
logout_args = {'next_page': '/'}

auth_patterns = [
    # API Views
    url(r'^token', ObtainAuthToken.as_view(), name='token'),
    url(r'^oauth2/(?P<backend>[^/]+)/token$', OAuthObtainAuthToken.as_view(),
        name='oauth2-token'),

    # Browsable API Views
    url(r'^login$', login, login_args, name='login'),
    url(r'^logout$', logout, logout_args, name='logout'),
]

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include(auth_patterns, namespace='rest_framework')),
]
