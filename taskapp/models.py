from django.db import models

# Create your models here.


class message_type(models.Model):
    key = models.IntegerField(unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class aws_query(models.Model):
    code = models.CharField(max_length=5, unique=True)
    title = models.CharField(max_length=255)


class Packet_Info(models.Model):
    packet_id = models.IntegerField(unique=True)
    packet_type = models.CharField(max_length=255, unique=True)


class weather_forecast_code(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)


class avalanche_grid(models.Model):
    grid_id = models.CharField(max_length=4)
    created_on = models.DateTimeField(auto_now_add=True)
