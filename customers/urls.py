from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from customers.views import (UserRegisterViewSet,
                             UserProfileAPIView,
                             ForgetPasswordAPIView)
from rest_framework.routers import DefaultRouter

app_name = 'customers'

router = DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='register')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='profile'),
    path('forget-password/', ForgetPasswordAPIView.as_view(), name='forget_password'),
] + router.urls
