from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, SmartBinViewSet, MaintenanceAlertViewSet, DepositLogViewSet, UserProfileView

router = DefaultRouter()
router.register(r'bins', SmartBinViewSet)
router.register(r'alerts', MaintenanceAlertViewSet)
router.register(r'deposit-logs', DepositLogViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]