from django.urls import path

from services.views import ServiceViewSet
from rest_framework.routers import DefaultRouter

app_name = 'services'

router = DefaultRouter()
router.register(r'service', ServiceViewSet, basename='service')

urlpatterns = router.urls
