from __future__ import unicode_literals

from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied


User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:  # pragma: no cover
                    raise serializers.ValidationError(
                        'User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError(
                    'Unable to login with provided credentials.')
        else:  # pragma: no cover
            raise serializers.ValidationError(
                'Must include "email" and "password"')


class AccessTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    access_token = serializers.CharField()

    def __init__(self, backend=None, **kwargs):
        self.backend = backend
        super(AccessTokenSerializer, self).__init__(**kwargs)

    def validate(self, attrs):
        access_token = attrs.get('access_token')

        try:
            user = self.backend.do_auth(access_token)
        except:
            raise PermissionDenied

        if user and user.email.lower() == attrs.get('email').lower():
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
            return attrs
        else:  # pragma: no cover
            raise serializers.ValidationError(
                'Unable to login with provided credentials.'
            )
