from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import time


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the attendance record and calculate late and overtime minutes."""

        attendance = serializer.save()

        if attendance.is_late:
            late_minutes = (attendance.check_in.hour - 8) * 60 + attendance.check_in.minute
            attendance.late_minutes = late_minutes
            attendance.save()

        if attendance.check_out and attendance.check_out > time(18, 0):
            overtime_minutes = (attendance.check_out.hour - 18) * 60 + attendance.check_out.minute
            attendance.overtime_minutes = overtime_minutes
            attendance.save()
