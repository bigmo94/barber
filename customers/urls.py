from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegisterViewSet, UserProfileViewSet
from rest_framework.routers import DefaultRouter

app_name = 'customers'

router = DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='register')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
