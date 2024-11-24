# apps/attendance/models.py

from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    is_late = models.BooleanField(default=False)
    worked_hours = models.FloatField()

    def __str__(self):
        return f'{self.user.username} - {self.check_in}'

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
