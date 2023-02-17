
from django.urls import path
from .import views



urlpatterns = [
    path("login/", views.wss_auth),
    path("dashboard/", views.ws_dashboard),
    path("connection/", views.ws_connect),
    path("history/", views.ws_connection_history),
    path("logout/", views.ws_logout),
    path("log-check/", views.socket_authentication),


]

