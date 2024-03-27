from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "common.views.error404"
handler500 = "common.views.error500"
