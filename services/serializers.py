from rest_framework import serializers

from services.models import EmployeeWorkingTime, Service


class ServiceMinimalSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='get_service_type_display', read_only=True)

    class Meta:
        model = Service
        fields = ['service_name', 'price', 'duration']


class ServiceSerializer(ServiceMinimalSerializer):
    class Meta:
        model = Service
        fields = ['service_name', 'price', 'discount', 'duration', 'description', 'created_time']


class EmployeeWorkingTimeDetailSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.username', read_only=True)
    store_name = serializers.CharField(source='employee.store.name', read_only=True)

    class Meta:
        model = EmployeeWorkingTime
        fields = ['id', 'employee_name', 'store_name', 'date', 'started_time', 'ended_time']


class EmployeeWorkingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeWorkingTime
        fields = ['employee', 'date', 'started_time', 'ended_time']
        extra_kwargs = {'employee': {'read_only': True}}

