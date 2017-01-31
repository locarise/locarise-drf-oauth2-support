# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from .views import ObtainAuthToken, OAuthObtainAuthToken


template_name = {'template_name': 'oauth2_client/login.html'}

next_page = {'next_page': '/'}


auth_patterns = [
    # API Views
    url(
        r'^token',
        ObtainAuthToken.as_view(),
        name='token'
    ),
    url(
        r'^oauth2/(?P<backend_name>[^/]+)/token$',
        OAuthObtainAuthToken.as_view(),
        name='oauth2-token'
    ),

    # Browsable API Views
    url(r'^login$', login, template_name, name='login'),
    url(r'^logout$', logout, next_page, name='logout'),
]

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include(auth_patterns, namespace='rest_framework')),
]
