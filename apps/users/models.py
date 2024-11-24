from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ("employee", "Employee"),
        ("admin", "Admin"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="employee")
    annual_leave = models.IntegerField(default=15)
    remaining_leave = models.IntegerField(default=15)
    position = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(null=True)
    last_leave_request = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="user",
    )
