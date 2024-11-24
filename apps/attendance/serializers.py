# apps/attendance/serializers.py

from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'check_in', 'check_out', 'is_late', 'worked_hours']
