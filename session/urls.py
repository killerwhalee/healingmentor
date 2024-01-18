from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'session'

urlpatterns = [
    path('', views.medass_index, name='index'),
    path('<str:username>', views.medass_inquiry, name='inquiry'),
    path('delete/<int:id>', views.medass_delete, name='delete')
]