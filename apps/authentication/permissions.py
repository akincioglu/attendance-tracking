from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Custom permission to only allow access to admins.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.role == "admin":
            return False

        return request.user


class IsEmployee(BasePermission):
    """
    Permission for employees.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.role == "employee":
            return False

        return request.user
