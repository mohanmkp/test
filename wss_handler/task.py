from celery import shared_task
from .models import Websocket_Status, ws_sessions, Receive_message, message_backup
from datetime import datetime
from channels.layers import get_channel_layer
from websocket import create_connection
import json
from .models import Receive_message
from celery.task.control import revoke
from django.core.cache import cache
import redis
from asgiref.sync import async_to_sync, sync_to_async
from chatapp.views import send_notification
from djqscsv import write_csv
import os
import ssl
import pathlib
import websockets
import asyncio

# ssl_dir = os.path.join(os.getcwd(), 'cert')
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# ssl_context.load_verify_locations(
#     pathlib.Path(__file__).with_name('server.pem'))
# ssl_context.check_hostname = False





async def connect_natsat_server(login_auth):
    try:
        async with websockets.connect('wss://38.242.219.47:8765/', ssl=ssl_context) as websocket:
            await websocket.send(login_auth)
            while True:
                msg = await websocket.recv()
                print(msg)

    except Exception as e:
        print("websocket connection fail because of", e)

    return "connection logout"


@shared_task
def wss_connector(username, password, packet_ids):
    login_auth = json.dumps({"sender": username, "password": password, "message_subscription": packet_ids})
    asyncio.run(connect_natsat_server(login_auth))

@shared_task(bind=True)
def sleepy(self, username, password, packet_ids):
    run_data = Websocket_Status.objects.last()
    if run_data.is_run is False:
        try:
            print("started")
            if cache.get("wss_task_id"):
                revoke(cache.get("wss_task_id"), terminate=True)
            try:
                r = redis.Redis(
                    host='127.0.0.1',
                    port=6379
                )
                r.flushdb()
            except Exception as e:
                print(e)
            cache.set("wss_task_id", self.request.id, timeout=2592000)

            ws = create_connection("ws://127.0.0.1:8005/auth/login/")
            ws.send(json.dumps({"sender": username, "password": password, "message_subscription": packet_ids}))
            run_data = Websocket_Status.objects.last()
            run_data.is_run = True
            run_data.started_at = datetime.now()
            run_data.save()
            data = ws.recv()
            print(data)
            try:
                ws_sessions.objects.create(
                    session_id=json.loads(data)['session_id'],
                    packet_id=packet_ids,
                    username=username,
                    password=password,
                    log_message=json.loads(data)['msg']
                )
            except Exception as e:
                ws_sessions.objects.create(
                    session_id="null",
                    packet_id=packet_ids,
                    username=username,
                    password=password,
                    log_message=data,
                    logout=True
                )

            print("here")
            while True:
                data = ws.recv()
                print("Received '%s'" % data)
                message = json.loads(data)
                try:
                    h = Receive_message(
                        data=data,
                        message_type=message["msg_type"],
                        aws_date=message["string_data"][4:10],
                        aws_time=message["string_data"][10:14],
                        station_id=message["string_data"][14:19],
                        sensor_code=message["string_data"][19:21],
                        packet_data=message["string_data"][21:len(message["string_data"]) - 2],
                        packet=message["string_data"]
                    )
                    h.save()
                except Exception as e:
                    print(e)
                    print(f"unknown message {data}")


        except Exception as e:
            run_data.is_run = False
            run_data.closed_at = datetime.now()
            run_data.save()
            data = ws_sessions.objects.last()
            data.logout_on = datetime.now()
            data.logout = True
            data.save()
            print("wss can not connect", e)
    else:
        print("already connected")





@shared_task
def logout_wss():
    print("ws logout")
    try:
        print("c;;")
        if cache.get("wss_task_id"):
            revoke(cache.get("wss_task_id"), terminate=True)
        data = ws_sessions.objects.last()
        data.logout_on = datetime.now()
        data.logout = True
        data.save()
        # asyncio.run(task_coroutine(False))
    finally:
        print("task kill done")




@shared_task
def try_to_wss_log():
    try:
        run_data = Websocket_Status.objects.last()
        ws_session = ws_sessions.objects.last()
        if run_data.is_run is False and ws_session.logout is False:
          print("calling", ws_session.username)
          sleepy.delay(ws_session.username, ws_session.password, ws_session.packet_id)

    except Exception as e:
        print(e)

    return "wss connection try"



@shared_task()
def data_backup():
    today_date = datetime.now().date()
    data = Receive_message.objects.filter(received_on__date=today_date).values(
        "message_type", "received_on", "data", "aws_date", "aws_time", "station_id",
        "sensor_code", "packet_data"
    )
    with open(f'media/backupdata/{today_date}.csv', 'wb') as csv_file:
        write_csv(data, csv_file)
        print(csv_file)
        message_backup.objects.create(
            file_path=csv_file.name,
            date=today_date
        )
    return "done"


@shared_task()
def message_ack():
    ws = create_connection("ws://127.0.0.1:9091/topic/public/notification/")
    while True:
        data = ws.recv()
        print(data)

