from django.urls import path
from django.contrib.auth import views as auth_views
from common import views

from django.shortcuts import render

app_name = "common"

urlpatterns = [
    # Login/Logout
    path(
        "login",
        auth_views.LoginView.as_view(template_name="common/login.html"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    # Signup
    path("signup", views.signup, name="signup"),
    # User profile
    path("profile", views.profile, name="profile"),
    # Download media
    path("download/<path:path>", views.download, name="download"),
]