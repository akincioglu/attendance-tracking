from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("admin/login/", views.AdminLoginView.as_view(), name="admin-login"),
    path("employee/login/", views.EmployeeLoginView.as_view(), name="employee-login"),
    path("admin/logout/", views.AdminLogoutView.as_view(), name="admin-logout"),
    path(
        "employee/logout/", views.EmployeeLogoutView.as_view(), name="employee-logout"
    ),
]
