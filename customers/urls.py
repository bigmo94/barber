from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from customers.views import (UserRegisterViewSet,
                             UserProfileAPIView,
                             ForgetPasswordAPIView,
                             StoreProfileAPIView,
                             StoreEmployeeViewSet,
                             EmployeeViewSet,
                             EmployeeWorkingTimeViewSet)
from rest_framework.routers import DefaultRouter

app_name = 'customers'

router = DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='register')
router.register(r'store-employee', StoreEmployeeViewSet, basename='store_employee')
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'employee-working-time', EmployeeWorkingTimeViewSet, basename='employee_working_time')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='profile'),
    path('forget-password/', ForgetPasswordAPIView.as_view(), name='forget_password'),
    path('store-profile/<int:pk>/', StoreProfileAPIView.as_view(), name='store_profile'),
] + router.urls
