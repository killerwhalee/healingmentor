from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "session"

urlpatterns = [
    path("", views.index, name="index"),
    # Guided Meditation
    path("gm/", views.gm_record, name="gm-record"),
    #path("gm/inquiry", views.gm_inquiry, name="gm-inquiry"),
    #path("gm/delete/<int:id>", views.gm_delete, name="gm-delete"),
    # Respiratory Graph
    path("rg/", views.rg_record, name="rg-record"),
    path("rg/inquiry", views.rg_inquiry, name="rg-inquiry"),
    path("rg/delete/<int:id>", views.rg_delete, name="rg-delete"),
    # Sustained Attention
    path("sa/", views.sa_record, name="sa-record"),
    path("sa/inquiry", views.sa_inquiry, name="sa-inquiry"),
    path("sa/delete/<int:id>", views.sa_delete, name="sa-delete"),
]
