from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from customers.models import Employee
from customers.tasks import send_verification_code_task
from customers.utils import code_generator
from message_handler.handler import get_message
from message_handler import messages

User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=255, write_only=True)

    def create(self, validated_data):
        phone = validated_data.get('phone')
        user = User.objects.filter(phone=phone).last()
        if not user:
            try:
                user = User.objects.create_user(**validated_data)
            except IntegrityError:
                raise ParseError(get_message(messages.ERROR_DUPLICATE_VALUE))
        if not user.is_enable:
            verify_code = code_generator()
            cache_key = 'login_code_{}'.format(phone)
            cache.set(cache_key, verify_code, timeout=120)
            send_verification_code_task.apply_async((user.phone, verify_code))

        return user


class VerifyUserSerializer(serializers.Serializer):
    verify_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        instance = self.instance
        cache_key = 'login_code_{}'.format(instance.phone)
        sent_code = cache.get(cache_key, None)
        input_code = attrs.get('verify_code')

        if sent_code and sent_code == input_code:
            return attrs
        else:
            raise ParseError(get_message(messages.ERROR_WRONG_VERIFY_CODE))


class UserSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'birthday', 'email',
                  'phone', 'gender_display', 'created_time', 'avatar']


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=120)


class VerifyResetPassCodeSerializer(ForgotPasswordSerializer):
    verify_code = serializers.IntegerField(write_only=True)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user__first_name', 'store__name']
