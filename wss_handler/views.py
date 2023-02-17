import time
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .forms import wss_session_form
from .models import Websocket_Status, message_backup
from .models import ws_sessions
import requests
import datetime
from .task import sleepy, logout_wss, wss_connector
from datetime import datetime

from dashboard.services.admin_decorator import admin_required




def socket_data():
    if cache.get("websocket_auth"):
        return cache.get("websocket_auth")
    else:
        return False


def socket_authentication(request):
    try:
        w_auth = Websocket_Status.objects.last()
        if w_auth.is_run is True:
           return JsonResponse({"message": "connected"})
        return JsonResponse({"message": "connection failed"})
    except Exception as e:
        return JsonResponse({"message": "connection failed"})



def wss_auth(request):
    websocket_auth = True
    if request.method == "POST":
        ws_form = wss_session_form(request.POST)
        if ws_form.is_valid():
            packet_id = ws_form.cleaned_data['packet_id']
            packet_ids = str(packet_id.split(",")).replace("[", "").replace("]", "")
            username = ws_form.cleaned_data["username"]
            password = ws_form.cleaned_data['password']
            confirmed = request.POST.get('confirm-yes')
            socket_status = Websocket_Status.objects.last()
            if socket_status.is_run is True and confirmed is None:
                already_connected = True
                return render(request, "dashboard/pages-login.html", locals())

            if confirmed is not None:
                sess = ws_sessions.objects.last()
                sess.logout_on = datetime.now()
                sess.logout = True
                sess.save()
                socket_status.is_run = False
                socket_status.closed_at = datetime.now()
                socket_status.save()
            # sleepy.delay(username, password, packet_ids)
            wss_connector.delay(username, password, packet_ids)
            return redirect("/wss/connection/")


    return render(request, "dashboard/pages-login.html", locals())








def ws_dashboard(request):
    wss_auth_data = ws_sessions.objects.last()
    ws_status = Websocket_Status.objects.last()

    return render(request, "sockets/dashboard.html", locals())



def ws_connect(request):
    return render(request, "sockets/new-connection.html", locals())

def ws_connection_history(request):
    w_auth = ws_sessions.objects.all()
    return render(request, "sockets/connection-history.html", locals())



def ws_logout(request):
    logout_wss.delay()
    run_data = Websocket_Status.objects.last()
    run_data.is_run = False
    run_data.closed_at = datetime.now()
    run_data.save()
    ws_session = ws_sessions.objects.last()
    ws_session.logout_on = datetime.now()
    ws_session.logout = True
    ws_session.save()
    return redirect("/wss/dashboard/")




