# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import ObtainAuthToken, OAuthObtainAuthToken


template_name = {'template_name': 'oauth2_client/login.html'}

next_page = {'next_page': '/'}

auth_patterns = patterns('django.contrib.auth.views',  # noqa
    # API Views
    url(r'^token', ObtainAuthToken.as_view(), name='token'),
    url(r'^oauth2/(?P<backend>[^/]+)/token$', OAuthObtainAuthToken.as_view(),
        name='oauth2-token'),

    # Browsable API Views
    url(r'^login$', 'login', template_name, name='login'),
    url(r'^logout$', 'logout', next_page, name='logout'),
)

urlpatterns = patterns('',   # noqa
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include(auth_patterns, namespace='rest_framework')),
)
