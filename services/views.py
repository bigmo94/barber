from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from customers.models import Employee
from customers.permissions import IsEmployee
from services.models import EmployeeWorkingTime
from services.serializers import EmployeeWorkingTimeSerializer, EmployeeWorkingTimeDetailSerializer
from message_handler.handler import get_message
from message_handler import messages


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
