from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permission for admins.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin


class IsEmployee(BasePermission):
    """
    Permission for employees.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_employee
