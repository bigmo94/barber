from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from customers.serializer import UserRegisterSerializer, VerifyUserSerializer

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
        tokens = instance.get_token()
        return Response(tokens)
