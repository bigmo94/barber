from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import mixins
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from customers.authentications import StoreAuthentication
from customers.models import Store, Employee, EmployeeWorkingTime
from customers.permissions import IsOwner, IsEnabled, IsEmployee
from customers.serializers import (UserRegisterSerializer,
                                   VerifyUserSerializer,
                                   UserSerializer,
                                   ForgotPasswordSerializer,
                                   VerifyResetPassCodeSerializer,
                                   StoreSerializer,
                                   EmployeeSerializer,
                                   EmployeeMinimalSerializer,
                                   EmployeeJustPatch,
                                   EmployeeWorkingTimeSerializer,
                                   EmployeeWorkingTimeDetailSerializer)
from customers.tasks import send_forget_pass_code_task
from customers.utils import code_generator
from message_handler import messages
from message_handler.handler import get_message

User = get_user_model()


class UserRegisterViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
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


class StoreProfileAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [StoreAuthentication]
    permission_classes = []
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_object(self):
        return self.request.store


class StoreEmployeeViewSet(viewsets.ModelViewSet):
    authentication_classes = [StoreAuthentication]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        return super().get_queryset().filter(store__client_id=self.request.store.client_id)

    def get_serializer_class(self):
        return {
            'create': EmployeeMinimalSerializer
        }.get(self.action, self.serializer_class)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data.get('user'))
        if user.is_employee:
            raise ParseError(get_message(messages.ERROR_USER_IS_EMPLOYEE))
        employee, created = Employee.objects.get_or_create(store=request.store, user=user)
        employee.services.set(serializer.validated_data.get('services'))
        user.is_employee = True
        user.save()
        return Response(get_message(messages.SUCCESS_EMPLOYEE_WAS_CREATED))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        user = instance.user
        user.is_employee = False
        user.save()
        return Response(get_message(messages.SUCCESS_EMPLOYEE_WAS_DELETED), status=status.HTTP_204_NO_CONTENT)


class EmployeeViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsOwner]
    http_method_names = ['get', 'patch', 'delete']

    def get_serializer_class(self):
        return {
            'partial_update': EmployeeJustPatch
        }.get(self.action, self.serializer_class)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(get_message(messages.SUCCESS_PROFILE_WAS_UPDATED))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        user = instance.user
        user.is_employee = False
        user.save()
        return Response(get_message(messages.SUCCESS_EMPLOYEE_WAS_DELETED), status=status.HTTP_204_NO_CONTENT)


class EmployeeWorkingTimeViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 mixins.UpdateModelMixin):
    queryset = EmployeeWorkingTime.objects.all()
    serializer_class = EmployeeWorkingTimeDetailSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        self.serializer_class = {
            "create": EmployeeWorkingTimeSerializer
        }.get(self.action, self.serializer_class)

        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset().filter(employee__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = Employee.objects.get(user=self.request.user)
        EmployeeWorkingTime.objects.get_or_create(employee=employee, **serializer.validated_data)
        return Response(get_message(messages.SUCCESS_WORKING_TIME_WAS_RECORDED))
