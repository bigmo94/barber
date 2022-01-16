from rest_framework import serializers

from services.models import Service


class ServiceMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_type', 'price', 'discount', 'duration', 'description']


class ServiceSerializer(ServiceMinimalSerializer):
    service_name = serializers.CharField(source='get_service_type_display', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'service_name', 'price', 'discount', 'duration', 'description', 'created_time']

