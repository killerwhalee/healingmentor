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

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "common.views.error400"
handler403 = "common.views.error403"
handler404 = "common.views.error404"
handler500 = "common.views.error500"
handler502 = "common.views.error502"
handler503 = "common.views.error503"
