from rest_framework import serializers
from .models import User
from django.db import transaction
from employees.models import Employee


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user
    


class OnboardingSerializer(serializers.Serializer):
    # User fields
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)

    # Employee fields
    employee_code = serializers.CharField(max_length=20)
    department = serializers.CharField(max_length=100)
    designation = serializers.CharField(max_length=100)
    employment_type = serializers.ChoiceField(choices=Employee.EmploymentType.choices)
    joining_date = serializers.DateField()
    basic_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    hra = serializers.DecimalField(max_digits=10, decimal_places=2)
    allowances = serializers.DecimalField(max_digits=10, decimal_places=2)
    deductions = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )
        return value

    def create(self, validated_data):
        with transaction.atomic():
            # Create User
            user = User.objects.create_user(
                email=validated_data["email"],
                full_name=validated_data["full_name"],
                role=validated_data["role"],
                password=validated_data["password"],
            )

            # Create Employee
            employee = Employee.objects.create(
                user=user,
                employee_code=validated_data["employee_code"],
                department=validated_data["department"],
                designation=validated_data["designation"],
                employment_type=validated_data["employment_type"],
                joining_date=validated_data["joining_date"],
                basic_salary=validated_data["basic_salary"],
                hra=validated_data["hra"],
                allowances=validated_data["allowances"],
                deductions=validated_data["deductions"],
            )

        return {
            "user_id": user.id,
            "employee_id": employee.id,
            "email": user.email,
        }

