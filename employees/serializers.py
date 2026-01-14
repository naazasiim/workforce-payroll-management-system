from rest_framework import serializers
from .models import Employee
from accounts.models import User


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "employee_code",
            "department",
            "designation",
            "employment_type",
            "joining_date",
            "exit_date",
            "basic_salary",
            "hra",
            "allowances",
            "deductions",
            "status",
            "is_active",
        ]

    def validate_status(self, value):
        if self.context["request"].user.role != User.Role.HR:
            raise serializers.ValidationError("Only HR can change status")
        return value
