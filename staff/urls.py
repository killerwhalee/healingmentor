from django.urls import path
from staff import views

app_name = "staff"

urlpatterns = [
    path("", views.index, name="index"),
    path("user", views.user, name="user"),
    path("session", views.session, name="session"),
]
