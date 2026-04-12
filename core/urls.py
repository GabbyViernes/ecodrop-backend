from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, SmartBinViewSet, MaintenanceAlertViewSet  

router = DefaultRouter()
router.register(r'bins', SmartBinViewSet)
router.register(r'alerts', MaintenanceAlertViewSet)    

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('', include(router.urls)),
]