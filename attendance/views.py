from django.db import transaction
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Attendance
from .serializers import AttendanceRecordSerializer
from employees.models import Employee

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsHRorManager



class BulkAttendanceView(APIView):
    """
    Mark attendance for multiple employees on a single date
    """
    permission_classes = [IsAuthenticated, IsHRorManager]
    
    def post(self, request):
        date = request.data.get("date")
        records = request.data.get("records", [])

        if not date:
            return Response(
                {"detail": "date is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date = parse_date(date)
        if not date:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(records, list) or not records:
            return Response(
                {"detail": "records must be a non-empty list"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attendance_objects = []

        with transaction.atomic():
            for record in records:
                serializer = AttendanceRecordSerializer(data=record)
                serializer.is_valid(raise_exception=True)

                employee = serializer.validated_data["employee"]

                # Prevent duplicate attendance
                if Attendance.objects.filter(employee=employee, date=date).exists():
                    return Response(
                        {
                            "detail": f"Attendance already marked for employee {employee.employee_code}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                attendance_objects.append(
                    Attendance(
                        employee=employee,
                        date=date,
                        status=serializer.validated_data.get("status"),
                        check_in=serializer.validated_data.get("check_in"),
                        check_out=serializer.validated_data.get("check_out"),
                        remarks=serializer.validated_data.get("remarks", ""),
                    )
                )

            Attendance.objects.bulk_create(attendance_objects)

        return Response(
            {"detail": "Attendance marked successfully"},
            status=status.HTTP_201_CREATED,
        )
