from rest_framework import serializers
from .models import Attendance


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "employee",
            "status",
            "check_in",
            "check_out",
            "remarks",
        ]
