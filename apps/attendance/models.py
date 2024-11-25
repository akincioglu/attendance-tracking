from django.db import models
from datetime import time, datetime
from apps.users.models import User


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    late_minutes = models.IntegerField(default=0)
    overtime_minutes = models.IntegerField(default=0)

    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    late_minutes = models.IntegerField(default=0)
    overtime_minutes = models.IntegerField(default=0)
    deducted_leave_minutes = models.IntegerField(default=0)

    @property
    def is_late(self) -> bool:
        """
        Checks if the attendance is late.
        """
        expected_check_in_time = time(8, 0)
        if self.check_in is not None:
            try:
                check_in_time = datetime.strptime(self.check_in, "%H:%M").time()
                if check_in_time > expected_check_in_time:
                    late_duration = datetime.combine(
                        self.date, check_in_time
                    ) - datetime.combine(self.date, expected_check_in_time)
                    self.late_minutes = int(late_duration.total_seconds() // 60)
                    return True
            except ValueError:
                pass
        return False

    def calculate_overtime(self) -> None:
        """
        Calculates overtime minutes.
        """
        expected_check_out = time(18, 0)
        try:
            check_out_time = datetime.strptime(self.check_out, "%H:%M").time()
        except (ValueError, TypeError):
            self.overtime_minutes = 0
        else:
            if check_out_time > expected_check_out:
                overtime_duration = datetime.combine(
                    self.date, check_out_time
                ) - datetime.combine(self.date, expected_check_out)
                self.overtime_minutes = int(overtime_duration.total_seconds() // 60)
            else:
                self.overtime_minutes = 0

    def __str__(self):
        return (
            f"{self.user.username} - {self.date} - {self.check_in} - {self.check_out}"
        )


class LeaveBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_days = models.FloatField(default=21.0)

    def deduct_leave(self, minutes):
        days_to_deduct = minutes / (8 * 60)  # Convert minutes to days
        self.total_days -= days_to_deduct
        self.save()


class LeaveType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="leave_requests"
    )
    leave_type = models.ForeignKey(
        LeaveType, on_delete=models.SET_NULL, null=True, blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_leaves",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date} ({self.status})"
