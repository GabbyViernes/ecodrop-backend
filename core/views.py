from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SmartBin, MaintenanceAlert, UserProfile, DepositLog
from .serializers import (
    RegisterSerializer, SmartBinSerializer, 
    MaintenanceAlertSerializer, DepositLogSerializer,
    UserProfileSerializer
)

@login_required(login_url='/accounts/login/')
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'user': request.user})

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class SmartBinViewSet(viewsets.ModelViewSet):
    queryset = SmartBin.objects.all()
    serializer_class = SmartBinSerializer

class MaintenanceAlertViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceAlert.objects.all()
    serializer_class = MaintenanceAlertSerializer

class DepositLogViewSet(viewsets.ModelViewSet):
    queryset = DepositLog.objects.all().order_by('-timestamp')
    serializer_class = DepositLogSerializer