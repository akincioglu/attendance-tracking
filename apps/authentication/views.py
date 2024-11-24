from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserLoginSerializer
from rest_framework.exceptions import AuthenticationFailed
from .permissions import IsAdmin, IsEmployee
from .serializers import UserRegistrationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegisterView(APIView):

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            200: openapi.Response("Successful login", UserRegistrationSerializer),
            400: "Invalid input",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh["role"] = user.role
            access_token = str(refresh.access_token)
            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                    "user_id": user.id,
                    "role": user.role,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin Login View
class AdminLoginView(APIView):
    """
    Login for admins.
    """

    permission_classes = []

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response("Successful login", UserLoginSerializer),
            400: "Invalid input",
        },
    )
    def post(self, request):
        """
        Login for admins.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        print(user.role)
        if not user.role == "admin":
            raise AuthenticationFailed("Only admins can login here.")
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


# Employee Login View
class EmployeeLoginView(APIView):
    """
    Login for employees.
    """

    permission_classes = []

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response("Successful login", UserLoginSerializer),
            400: "Invalid input",
        },
    )
    def post(self, request):
        """
        Login for employees.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if not user.role != "employee":
            raise AuthenticationFailed("Only employees can login here.")
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


# Admin Logout View
class AdminLogoutView(APIView):
    """
    Logout for admins.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin:
            raise AuthenticationFailed("Only admins can logout here.")
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            raise AuthenticationFailed("No refresh token provided")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Employee Logout View
class EmployeeLogoutView(APIView):
    """
    Logout for employees.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_employee:
            raise AuthenticationFailed("Only employees can logout here.")
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            raise AuthenticationFailed("No refresh token provided")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
