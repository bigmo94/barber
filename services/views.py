from rest_framework import viewsets
from rest_framework.response import Response

from customers.authentications import StoreAuthentication
from services.models import Service
from services.serializers import (ServiceSerializer,
                                  ServiceMinimalSerializer)
from message_handler.handler import get_message
from message_handler import messages


class ServiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [StoreAuthentication]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return super().get_queryset().filter(store__client_id=self.request.store.client_id)

    def get_serializer_class(self):
        return {
            'create': ServiceMinimalSerializer
        }.get(self.action, self.serializer_class)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = request.store
        Service.objects.create(store=store, **serializer.validated_data)
        return Response(get_message(messages.SUCCESS_SERVICE_WAS_CREATED))
