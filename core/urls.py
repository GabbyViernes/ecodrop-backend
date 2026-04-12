from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, SmartBinViewSet

# A router automatically builds URLs for our ModelViewSet
router = DefaultRouter()
router.register(r'bins', SmartBinViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'), # Built-in token login
    path('', include(router.urls)),
]