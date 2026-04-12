from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .models import SmartBin
from .serializers import RegisterSerializer, SmartBinSerializer

# Auth Endpoint: Logic for registering a user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# Feature Endpoints: Automatically handles GET, POST, PUT, DELETE for bins
class SmartBinViewSet(viewsets.ModelViewSet):
    queryset = SmartBin.objects.all()
    serializer_class = SmartBinSerializer
