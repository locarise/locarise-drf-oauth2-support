# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers, renderers, permissions

from social_core.backends.utils import get_backend
from social_core.exceptions import MissingBackend

from .serializers import AuthTokenSerializer, AccessTokenSerializer


User = get_user_model()


class ObtainAuthToken(APIView):
    """
    This authentication scheme uses a simple token-based HTTP Authentication
    scheme.

    For clients to authenticate, the token key should be included in the
    `Authorization` HTTP header. The key should be prefixed by the string
    literal "Token", with whitespace separating the two strings. For example:

        Authorization: Token abc123

    Unauthenticated responses that are denied permission will result in an
    `HTTP 401` Unauthorized response with an appropriate WWW-Authenticate
    header.
    """
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token
    queryset = Token.objects.none()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.validated_data['user']
            )
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OAuthObtainAuthToken(APIView):
    """
    This authentication scheme uses the oauth2 access token from the given
    authentication backend to authenticate the user.
    """
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AccessTokenSerializer
    model = Token
    queryset = Token.objects.none()

    def get_backend_instance(self, name=None, strategy=None):
        try:
            backend = get_backend(
                backends=settings.AUTHENTICATION_BACKENDS,
                name=name
            )
        except MissingBackend:
            raise Http404
        return backend(strategy=strategy)

    def post(self, request, backend_name, *args, **kwargs):
        backend = self.get_backend_instance(name=backend_name)

        serializer = self.serializer_class(
            data=request.data,
            backend=backend
        )
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.validated_data['user']
            )
            return Response({'token': token.key})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
