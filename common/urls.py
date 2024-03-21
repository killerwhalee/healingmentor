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
    path("terms", views.terms, name="terms"),
    # User profile
    path("profile/<str:username>", views.profile, name="profile"),
    # Download media
    path("download/<path:path>", views.download, name="download"),
    # Tests
    path("404", lambda _: render(_, "error/404.html")),
]
