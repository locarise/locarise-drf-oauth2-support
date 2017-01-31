# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    Read only serializer for providing user information at login.
    """
    uid = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    locale = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    organization_set = serializers.JSONField(read_only=True)

    class Meta:
        model = User
        fields = ('uid', 'email', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'locale', 'created_at', 'organization_set')
