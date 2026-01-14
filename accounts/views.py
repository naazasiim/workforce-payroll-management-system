from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsHRorManager
from .serializers import OnboardingSerializer


class UserCreateView(APIView):
    # permission_classes = [IsAuthenticated, IsHRorManager]

    def post(self, request):
        password = request.data.get("password")
        if not password:
            return Response(
                {"password": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            full_name=serializer.validated_data["full_name"],
            role=serializer.validated_data["role"],
            password=password,
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        users = User.objects.all()

        role = request.query_params.get("role").upper()
        if role:
            users = users.filter(role=role)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OnboardingView(APIView):
    permission_classes = [IsAuthenticated, IsHRorManager]

    def post(self, request):
        serializer = OnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
