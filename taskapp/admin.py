from django.contrib import admin
from .models import message_type, aws_query, Packet_Info, weather_forecast_code, avalanche_grid
# Register your models here.




class Message_type(admin.ModelAdmin):
    list_display = ["key", "value"]

admin.site.register(message_type, Message_type)



class aws(admin.ModelAdmin):
    list_display = ["code", "title"]

admin.site.register(aws_query, aws)


class packet(admin.ModelAdmin):
    list_display = ["packet_id", "packet_type"]

admin.site.register(Packet_Info, packet)

class weather_forecast(admin.ModelAdmin):
    list_display = ["code", "title"]

admin.site.register(weather_forecast_code, weather_forecast)

class avalanche_grids(admin.ModelAdmin):
    list_display = ["grid_id", "created_on"]

admin.site.register(avalanche_grid, avalanche_grids)
