from django.db import models
import random
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
# Create your models here.



class ws_sessions(models.Model):
    connect_on = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=255)
    packet_id = models.CharField(max_length=100)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    logout_on = models.DateTimeField(null=True, blank=True)
    logout = models.BooleanField(default=False)
    log_message = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.session_id



class Receive_message(models.Model):
    received_on = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=255)
    message_type = models.CharField(max_length=2)
    aws_date = models.CharField(max_length=6)
    aws_time = models.CharField(max_length=4)
    station_id = models.CharField(max_length=5)
    sensor_code = models.CharField(max_length=2)
    packet_data = models.CharField(max_length=117)
    packet = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.message_type



class Running_details(models.Model):
    is_run = models.BooleanField(default=False)
    started_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)


class Websocket_Status(models.Model):
    is_run = models.BooleanField(default=False)
    started_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)



class Query_Send_Message(models.Model):
    send_on = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=117)
    terminal_id = models.CharField(max_length=5)
    query_code = models.CharField(max_length=2)
    message_date = models.CharField(max_length=6)
    end_time = models.CharField(max_length=4)
    current_date = models.CharField(max_length=6)
    current_time = models.CharField(max_length=4)
    sequence_num = models.IntegerField()
    send_data = JSONField(null=True, blank=True)
    ack = models.BooleanField(null=True, blank=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)





class message_backup(models.Model):
    create_on = models.DateTimeField(auto_now=True)
    date = models.DateField()
    file_path = models.CharField(max_length=255, null=True, blank=True)


class command_message(models.Model):
    received_on = models.DateTimeField(auto_now=True)
    current_date = models.CharField(max_length=6)
    current_time = models.CharField(max_length=4)
    terminal_id = models.CharField(max_length=5)
    command_code = models.CharField(max_length=2)
    query_message = models.CharField(max_length=12)
    data = models.CharField(max_length=117)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


class reboot_message(models.Model):
    send_on = models.DateTimeField(auto_now=True)
    current_date = models.CharField(max_length=6)
    current_time = models.CharField(max_length=4)
    terminal_id = models.CharField(max_length=5)
    reboot_code = models.CharField(max_length=2)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


class Weather_Forecast_Message(models.Model):
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    send_on = models.DateTimeField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    num_of_forecast_day = models.CharField(max_length=2)
    forecast_area = models.CharField(max_length=3)
    day_1 = models.CharField(max_length=2)
    day_2 = models.CharField(max_length=2)
    day_3 = models.CharField(max_length=2)
    day_4 = models.CharField(max_length=2)
    day_5 = models.CharField(max_length=2)
    day_6 = models.CharField(max_length=2)
    packet = models.CharField(max_length=255,null=True, blank=True)


class site_critical_alert(models.Model):
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    send_on = models.DateTimeField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    packet = models.CharField(max_length=255)
    num_of_day = models.CharField(max_length=2)
    avalanche_axis_id = models.CharField(max_length=3)
    alert_message = models.TextField(max_length=100)


class Avalanche_message_one(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to="avalanche_files/", null=True, blank=True)
    ack = models.BooleanField(null=True, blank=True)
    sequence_num = models.IntegerField()
    message_on = models.DateTimeField(auto_now_add=True)
    data = JSONField()
    packet = models.CharField(max_length=255)
    message_type = models.IntegerField(default=91)
    start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    num_of_axis = models.IntegerField(range(1, 16))
    axis_ids = JSONField(null=True, blank=True)
    forecast_codes = JSONField(null=True, blank=True)



class Avalanche_message_two(models.Model):
    avalanche_one = models.ForeignKey(Avalanche_message_one, on_delete=models.DO_NOTHING)
    message_type = models.IntegerField(default=98)
    forecast_start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    outlook = models.CharField(max_length=124)




