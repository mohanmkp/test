from django.urls import path, include, re_path
from .import views

urlpatterns = [

    path("send-avalanche/", views.send_avalanche_forecast, name="message_sender"),
    path("hourly-data/", views.hourly_data_show),
    path("query-data/", views.data_query_show),
    path("health-query/", views.health_query_show),
    path("send-query/", views.send_query_message),
    path("data-logger/", views.data_logger),
    path("manual-data/", views.manual_data),
    path("health-query-code3/", views.health_query_code_three),
    path("show-send-query-message/", views.show_send_query_message),
    path("show-message-code-details/", views.message_type_info),
    path("show-aws-message-code-details/", views.aws_message_info),
    path("send-command/", views.send_command_message),
    path("send-reboot/", views.send_reboot_message),
    path("send-weather-forecast/", views.send_weather_forecast),
    path("show-backups/", views.message_backup_info),
    path('show-send-weather-messages/', views.show_send_weather),
    path('send-critical-alert/', views.send_critical_alert),
    path('show-critical-alert/', views.show_critical_messages),
    path('avalanche-axis-update/', views.avalanche_axis_update),
    path('avalanche-code-update/', views.avalanche_code_update),
    path('weather-area-update/', views.weather_area_update),
    path('weather-code-update/', views.weather_code_update),

]

