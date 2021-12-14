from rest_framework import viewsets, generics
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from customers.serializer import (UserRegisterSerializer,
                                  VerifyUserSerializer,
                                  UserSerializer, )
from customers.permissions import IsActivated, IsOwner

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
        instance.is_active = True
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
    permission_classes = [IsAuthenticated, IsActivated, IsOwner]
    serializer_class = UserSerializer
