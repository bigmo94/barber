from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from customers.tasks import send_verification_code_task
from customers.utils import code_generator

User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=255, write_only=True)

    def create(self, validated_data):
        phone = validated_data.get('phone')
        user = User.objects.filter(phone=phone).last()
        if not user:
            user = User.objects.create_user(**validated_data)
        if not user.is_active:
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
            raise ValidationError('Wrong verify code')
