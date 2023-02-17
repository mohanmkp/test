from django.db import models
from django.contrib.auth.models import User

# Create your models here.

types = (("avalanche", "avalanche"), ("rain", "rain"))


class Pointers(models.Model):
    title = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    station_id = models.CharField(max_length=50, null=True, blank=True)
    terminal_id = models.CharField(max_length=200, null=True, blank=True)
    typee = models.CharField(max_length=200, choices=types, null=True, blank=True)
    filee = models.FileField(upload_to="filess",null=True, blank=True) 
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "pointer"
        unique_together = ('longitude', 'latitude',)


class GeoFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    g_json_file = models.FileField(upload_to="mapdata")
    create_at = models.DateField(auto_now_add=True)
    
