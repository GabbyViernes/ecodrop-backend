from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .models import SmartBin, MaintenanceAlert          
from .serializers import RegisterSerializer, SmartBinSerializer, MaintenanceAlertSerializer  

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class SmartBinViewSet(viewsets.ModelViewSet):
    queryset = SmartBin.objects.all()
    serializer_class = SmartBinSerializer

class MaintenanceAlertViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceAlert.objects.all()
    serializer_class = MaintenanceAlertSerializer