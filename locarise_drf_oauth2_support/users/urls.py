# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import CurrentUserView


urlpatterns = patterns('',   # noqa
    url(r'^current-user$', CurrentUserView.as_view(), name='current-user'),
    url(r'^me$', CurrentUserView.as_view(), name='me')
)
