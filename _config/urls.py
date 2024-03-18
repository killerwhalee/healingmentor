from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # System/Root Application
    path("admin/", admin.site.urls),
    # Home Redirection
    path("", lambda _: redirect("home/")),
    # General Purpose Application
    path("home/", include("home.urls")),
    path("common/", include("common.urls")),
    # User Purpose Application
    path("session/", include("session.urls")),
]
