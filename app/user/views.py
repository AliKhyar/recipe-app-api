#from django.shortcuts import render
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """create a new user"""
    serializer_class = UserSerializer
    

class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication,TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated)

    def get_object(self):
        """get and retrieve authenticated user"""
        return self.request.user