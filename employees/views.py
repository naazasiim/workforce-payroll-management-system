from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsHRorManager
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.select_related("user")
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsHRorManager]
