# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth.views import LoginView, LogoutView

from .views import OAuthObtainAuthToken, ObtainAuthToken

template_name = "oauth2_client/login.html"

next_page = "/"

auth_patterns = [
    # API Views
    url(r"^token", ObtainAuthToken.as_view(), name="token"),
    url(
        r"^oauth2/(?P<backend_name>[^/]+)/token$",
        OAuthObtainAuthToken.as_view(),
        name="oauth2-token",
    ),
    # Browsable API Views
    url(r"^login$", LoginView.as_view(template_name=template_name), name="login"),
    url(r"^logout$", LogoutView.as_view(template_name=next_page), name="logout"),
]

urlpatterns = [
    url("", include(("social_django.urls", "rest_framework"), namespace="social")),
    url(
        r"^auth/",
        include((auth_patterns, "rest_framework"), namespace="rest_framework"),
    ),
]
