from rest_framework import serializers
from .models import Attendance, LeaveBalance, LeaveType, LeaveRequest


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "user",
            "date",
            "check_in",
            "check_out",
            "late_minutes",
            "overtime_minutes",
            "deducted_leave_minutes",
        ]
        read_only_fields = [
            "late_minutes",
            "overtime_minutes",
            "deducted_leave_minutes",
        ]


class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = ["id", "user", "total_days"]


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = "__all__"
        read_only_fields = ["approved_by", "created_at", "updated_at"]
