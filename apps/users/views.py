from rest_framework import viewsets
from .serializers import UserSerializer
from apps.users.models import User
from apps.authentication.permissions import IsAdmin
from apps.authentication.authentication import CustomJWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users with admin permissions."""

    authentication_classes = [CustomJWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def list(self, request, *args, **kwargs):
        print(request.user)
        return super().list(request, *args, **kwargs)
