from rest_framework import serializers

class EmployeeReportSerializer(serializers.Serializer):
    employee = serializers.DictField()
    attendance_summary = serializers.DictField()
    leave_summary = serializers.DictField()
    payroll = serializers.DictField()
