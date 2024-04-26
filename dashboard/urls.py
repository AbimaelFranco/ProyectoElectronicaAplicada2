from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard, name="Dashboard"),
    path('historial', views.Historial, name="Historial"),
    path('user_config', views.User_config, name="User_config"),
]
