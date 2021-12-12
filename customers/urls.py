from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegisterViewSet
from rest_framework.routers import DefaultRouter

app_name = 'customers'

router = DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='register')

urlpatterns = [
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
