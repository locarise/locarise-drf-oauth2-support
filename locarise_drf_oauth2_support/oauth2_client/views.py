# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import __version__

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers, renderers

from social.backends.utils import get_backend
from social.exceptions import WrongBackend

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
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.object['user'])
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OAuthObtainAuthToken(APIView):
    """
    This authentication scheme uses the oauth2 access token from the given
    authentication backend to authenticate the user.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AccessTokenSerializer
    model = Token

    def post(self, request, backend, *args, **kwargs):
        backend = request.social_backend = get_backend(backend, request)
        if request.social_backend is None:
            raise WrongBackend(backend)
        serializer = self.serializer_class(data=request.data, backend=backend)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.object['user'])
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
