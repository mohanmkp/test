from django.contrib import admin
from .models import ws_sessions, Receive_message, Websocket_Status, Query_Send_Message, message_backup,\
     command_message, reboot_message, site_critical_alert, Avalanche_message_one, Avalanche_message_two
# Register your models here.




class receiver_sms(admin.ModelAdmin):
    list_display = ["id", "received_on", "packet_data", "data"]

admin.site.register(Receive_message, receiver_sms)
admin.site.register(ws_sessions)


class running_detail(admin.ModelAdmin):
    list_display = ["id", "started_at", "closed_at", "is_run"]

admin.site.register(Websocket_Status, running_detail)

class query_message(admin.ModelAdmin):
    list_display = ['id', "data", "send_by", "ack"]
admin.site.register(Query_Send_Message, query_message)
admin.site.register(message_backup)
admin.site.register(command_message)
admin.site.register(reboot_message)
admin.site.register(site_critical_alert)
admin.site.register(Avalanche_message_one)
admin.site.register(Avalanche_message_two)



