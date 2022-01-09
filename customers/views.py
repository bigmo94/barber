from django.core.cache import cache
from rest_framework import viewsets, generics
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ParseError

from customers.utils import code_generator
from customers.tasks import send_forget_pass_code_task
from customers.serializer import (UserRegisterSerializer,
                                  VerifyUserSerializer,
                                  UserSerializer,
                                  ForgotPasswordSerializer,
                                  VerifyResetPassCodeSerializer, )
from customers.permissions import IsOwner, IsEnabled
from message_handler.handler import get_message
from message_handler import messages

User = get_user_model()


class UserRegisterViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin):
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        return {
            'create': UserRegisterSerializer,
            'verify': VerifyUserSerializer
        }.get(self.action)

    @action(detail=True, methods=['post'])
    def verify(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.is_enable = True
        instance.save()
        refresh_token = RefreshToken.for_user(instance)
        tokens = {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token)
        }
        return Response(tokens)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEnabled, IsOwner]
    serializer_class = UserSerializer


class ForgetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=serializer.validated_data.get('username'))
        except User.DoesNotExist:
            raise ParseError(get_message(messages.ERROR_NOT_FOUND_ANY_USER_BY_THIS_USERNAME))

        verify_code = code_generator()
        cache_key = 'forget_pass_code_{}'.format(user.phone)
        cache.set(cache_key, verify_code, timeout=120)
        send_forget_pass_code_task.apply_async((user.phone, verify_code))

        return Response(get_message(messages.SUCCESS_RESET_CODE_WAS_SENT))


class VerifyResetPassCodeAPIView(generics.GenericAPIView):
    serializer_class = VerifyResetPassCodeSerializer

    # TODO this part must be change
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=serializer.validated_data.get('username'))
        except User.DoesNotExist:
            raise ParseError(get_message(messages.ERROR_NOT_FOUND_ANY_USER_BY_THIS_USERNAME))

        cache_key = 'forget_pass_code_{}'.format(user.phone)
        sent_code = cache.get(cache_key, None)
        input_code = serializer.validated_data.get('verify_code')

        if sent_code and sent_code == input_code:
            return Response('ok')
        else:
            raise ParseError(get_message(messages.ERROR_WRONG_VERIFY_CODE))


