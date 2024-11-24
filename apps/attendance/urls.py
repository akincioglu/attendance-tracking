from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AttendanceViewSet,
    EmployeeInfoViewSet,
    LeaveBalanceViewSet,
    LeaveRequestViewSet,
    LeaveTypeViewSet,
)

router = DefaultRouter()
router.register(r"", AttendanceViewSet, basename="attendance")
router.register(r"leave-balance", LeaveBalanceViewSet, basename="leave-balance")
router.register(r"leave-types", LeaveTypeViewSet)
router.register(r"leave-requests", LeaveRequestViewSet)
router.register(r"employee-info", EmployeeInfoViewSet, basename="employee-info")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "leave-balance/report/",
        LeaveBalanceViewSet.as_view({"get": "monthly_report"}),
        name="monthly-report",
    ),
]
