from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.timezone import now
from apps.authentication.authentication import CustomJWTAuthentication
from apps.authentication.permissions import IsAdmin, IsAuthenticated, IsEmployee
from apps.users.models import User
from apps.users.serializers import UserSerializer
from .models import Attendance, LeaveBalance, LeaveRequest, LeaveType
from .serializers import (
    AttendanceSerializer,
    LeaveBalanceSerializer,
    LeaveRequestSerializer,
    LeaveTypeSerializer,
)
from .services import process_attendance

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action


class AttendanceViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        """
        Filter queryset by user_id and date.
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        date = self.request.query_params.get("date")

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if date:
            queryset = queryset.filter(date=date)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="Filter by user ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Filter by date (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        List all attendance records for the current user.

        Returns:
            A list of serialized Attendance objects in the response body.
        """
        print(request.user.role)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new attendance record for the current user.

        This method creates a new attendance record with the current user, given
        check_in and check_out times. The request should include the check_in and
        check_out times, in the format "HH:MM".

        Returns:
            A serialized Attendance object in the response body.
        """
        user = request.user
        check_in = request.data.get("check_in")
        check_out = request.data.get("check_out")

        attendance = process_attendance(user, check_in, check_out)
        serializer = self.get_serializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LeaveBalanceViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer

    def get_queryset(self):
        """
        Filter queryset by user_id.
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a user's leave balance.

        Returns:
            A serialized LeaveBalance object in the response body.
        """
        leave_balance = LeaveBalance.objects.get(user=request.user)
        serializer = self.get_serializer(leave_balance)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="Filter by user ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "month",
                openapi.IN_QUERY,
                description="Filter by month (format: YYYY-MM)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
        ],
        operation_description="Calculate monthly report for a specific user.",
        responses={
            200: openapi.Response(
                description="Monthly report",
                content={
                    "application/json": {
                        "example": {
                            "total_late_minutes": 0,
                            "total_overtime_minutes": 0,
                            "total_days_worked": 0,
                        }
                    }
                },
            ),
        },
    )
    @action(methods=["get"], detail=False)
    def monthly_report(self, request, user_id=None, month=None):
        """
        Calculate monthly report for a specific user.
        """
        user_id = request.query_params.get("user_id", user_id)
        month = request.query_params.get("month", datetime.now().strftime("%Y-%m"))
        month_date = datetime.strptime(month, "%Y-%m")
        print(user_id, month_date)
        attendances = Attendance.objects.filter(
            user_id=user_id, date__year=month_date.year, date__month=month_date.month
        )
        total_late = sum(a.late_minutes for a in attendances)
        total_overtime = sum(a.overtime_minutes for a in attendances)

        return Response(
            {
                "total_late_minutes": total_late,
                "total_overtime_minutes": total_overtime,
                "total_days_worked": attendances.count(),
            }
        )


class LeaveTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class LeaveRequestViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return LeaveRequest.objects.filter(user=user)
        return LeaveRequest.objects.none()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsEmployee() | IsAdmin()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new leave request.

        This action allows an employee to create a new leave request. The request
        data should include details such as leave type, start date, end date, and
        reason for the leave. The request is validated and saved, with the current
        user set as the requester.

        Returns:
            A serialized LeaveRequest object in the response body with a 201 status
            code upon successful creation. If there's an error during creation, a
            400 status code with an error message is returned.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=True,
        methods=["put"],
        permission_classes=[IsAdmin],
    )
    def update_status(self, request, pk):
        """
        Update the status of a leave request.
        """
        leave_request = self.get_object()
        status = request.data.get("status")
        if status not in ["approved", "rejected"]:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave_request.status = status
        leave_request.approved_by = request.user
        leave_request.save()
        return Response(
            {"message": f"Leave request {status} successfully."},
            status=status.HTTP_200_OK,
        )


class EmployeeInfoViewSet(viewsets.ViewSet):
    """
    A viewset to retrieve all employees' leave requests and personal details.
    Accessible only by admin users.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request):
        """
        List all employees' personal information and leave requests.
        """

        employees = User.objects.all(role="employee")
        employees_data = []

        for employee in employees:
            leave_requests = LeaveRequest.objects.filter(user=employee)

            employee_data = {
                "personal_info": UserSerializer(employee).data,
                "leave_requests": LeaveRequestSerializer(
                    leave_requests, many=True
                ).data,
            }
            employees_data.append(employee_data)

        return Response(employees_data, status=200)
