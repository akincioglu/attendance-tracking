from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Permission for authenticated users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAdmin(BasePermission):
    ...

    def has_permission(self, request, view):
        print("Checking admin permission...")
        if not request.user.is_authenticated:
            print("User is not authenticated")
            return False

        print("User role:", request.user.role)
        return request.user.role == "admin"


class IsEmployee(BasePermission):
    ...

    def has_permission(self, request, view):
        print("Checking employee permission...")
        if not request.user.is_authenticated:
            print("User is not authenticated")
            return False

        print("User role:", request.user.role)
        return request.user.role == "employee"
