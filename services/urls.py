from django.urls import path

from services.views import EmployeeWorkingTimeViewSet
from rest_framework.routers import DefaultRouter

app_name = 'services'

router = DefaultRouter()
router.register(r'working-time', EmployeeWorkingTimeViewSet, basename='working-time')

urlpatterns = router.urls
