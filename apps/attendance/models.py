# src/api/v1/modules/attendance/models.py
from django.db import models
from django.contrib.auth import get_user_model
from datetime import time


class Attendance(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    late_minutes = models.IntegerField(default=0)  # Geç kalma süresi
    overtime_minutes = models.IntegerField(default=0)  # Fazla mesai süresi

    @property
    def is_late(self):
        return self.check_in and self.check_in > time(8, 0)

    def __str__(self):
        return (
            f"{self.user.username} - {self.date} - {self.check_in} - {self.check_out}"
        )
