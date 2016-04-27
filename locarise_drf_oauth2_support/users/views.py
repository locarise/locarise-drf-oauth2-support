# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import generics

from .serializers import CurrentUserSerializer


User = get_user_model()


class CurrentUserView(generics.RetrieveAPIView):
    """
    Retrieve authenticated user information.
    """
    model = User
    serializer_class = CurrentUserSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user
