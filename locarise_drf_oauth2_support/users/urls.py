# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import CurrentUserView


urlpatterns = [
    url(r'^me$', CurrentUserView.as_view(), name='me')
]
