from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import message_type, aws_query, weather_forecast_code
from dashboard.services.admin_decorator import admin_required
from wss_handler.models import Receive_message, Query_Send_Message, command_message, reboot_message, ws_sessions, message_backup, \
    Weather_Forecast_Message, site_critical_alert
from datetime import datetime
import time
from asgiref.sync import async_to_sync
from chatapp.views import send_message_query, send_message_to_natsat
from taskapp.services.query_sequence import send_query_sequence_generator
from taskapp.services.command_sequence import command_sequence_generator
from taskapp.services.reboot_sequence import reboot_sequence_generator
from taskapp.services.weather_forecast import weather_forecast
from taskapp.services.critical_message import critical_alert
from .services.avalanche_forecast import avalanche_forecaster_message_one, avalanche_forecaster_message_two


@login_required(login_url='/login/')
def send_avalanche_forecast(request):
    if request.method == "POST":
        # message 1
        message_code = 91
        start_date = request.POST['start_date']
        grid_id = request.POST['grid_id']
        num_axis = request.POST['num_axis']
        axis_ids = request.POST.getlist("avalanche-axis-id")
        forecast_codes = request.POST.getlist("forecast_codes")
        current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        format_date = datetime.strftime(current_date, "%d%m%y")
        message1 = avalanche_forecaster_message_one(
            request.user,
            format_date,
            grid_id,
            num_axis,
            axis_ids,
            forecast_codes
        )
        # message 2
        message_code2 = 98
        outlook = request.POST['outlook']

        avalanche_forecaster_message_two(
            message_one=message1,
            start_date=format_date,
            grid_id=grid_id,
            outlook=outlook
        )

    message_types = message_type.objects.all()
    return render(request, "messages/send_avalanche.html", locals())




@login_required(login_url='/login/')
def hourly_data_show(request):
    messages = Receive_message.objects.filter(message_type="72")
    return render(request, "messages/hourly-data.html", locals())





@login_required(login_url='/login/')
def data_query_show(request):
    messages = Receive_message.objects.filter(message_type="73").order_by("-id")
    return render(request, "messages/data-query.html", locals())



@login_required(login_url='/login/')
def health_query_show(request):
    messages = Receive_message.objects.filter(message_type="74")
    return render(request, "messages/health-query.html", locals())



@login_required(login_url='/login/')
def data_logger(request):
    messages = Receive_message.objects.filter(message_type="70")
    return render(request, "messages/data-logger.html", locals())

@login_required(login_url='/login/')
def manual_data(request):
    messages = Receive_message.objects.filter(message_type="71")
    return render(request, "messages/mannul-data.html", locals())


@login_required(login_url='/login/')
def health_query_code_three(request):
    messages = Receive_message.objects.filter(message_type="75")
    return render(request, "messages/health-query3.html", locals())





@login_required(login_url="/login/")
def send_query_message(request):
    aws_query_code = aws_query.objects.all()
    if request.method == "POST":
        query_code = request.POST['aws_query']
        terminal_id = request.POST['terminal_id']
        message_date = request.POST['message_date']
        end_time = request.POST['end_time']

        date = datetime.strptime(str(message_date), '%Y-%m-%d').date()
        m_date = datetime.strftime(date, "%d%m%y")
        time_temp = datetime.strptime(end_time, "%H:%M").time()
        e_time = time_temp.strftime("%H%M")
        current_data = datetime.now()
        current_date = datetime.strftime(current_data, "%d%m%y")
        current_time = datetime.strftime(current_data, "%H%M")
        try:
          message_code = message_type.objects.filter(value="query_message").last().key
        except Exception as e:
            print(e)
            message_code = 60
        message_encode = f"#@{message_code}{current_date}{current_time}{terminal_id}{query_code}{m_date}{e_time}@#"
        sequence_num = send_query_sequence_generator()

        db_data = Query_Send_Message.objects.create(
            data=message_encode,
            terminal_id=terminal_id,
            query_code=query_code,
            message_date=m_date,
            end_time=e_time,
            current_date=current_date,
            current_time=current_time,
            sequence_num=sequence_num,
            send_by=request.user
        )
        try:
          resp = async_to_sync(send_message_query)(message_encode, request.user.username, sequence_num)
        except Exception as e:
            print(e)

        return redirect("/message/send-query/")


    return render(request, "messages/send-query.html", locals())


@login_required(login_url="/login/")
def show_send_query_message(request):
    messages = Query_Send_Message.objects.all()
    return render(request, "messages/show-send-query-message.html", locals())


@login_required(login_url="/login/")
def message_type_info(request):
    messages = message_type.objects.all()
    return render(request, "messages/message-code-info.html", locals())


@login_required(login_url="/login/")
def aws_message_info(request):
    messages = aws_query.objects.all()
    return render(request, "messages/view-aws-code.html", locals())



@login_required(login_url="/login/")
def send_command_message(request):
    if request.method == "POST":
        mess_type = 61
        terminal_id = request.POST["terminal_id"]
        command_code = request.POST["command_code"]
        query_message = request.POST["query_message"]
        current_data = datetime.now()
        current_date = datetime.strftime(current_data, "%d%m%y")
        current_time = datetime.strftime(current_data, "%H%M")
        sequence_num = command_sequence_generator()
        string_message = f"#@{mess_type}{current_date}{current_time}{terminal_id}{command_code}{query_message}@#"
        session_data = ws_sessions.objects.last()
        if session_data.logout is False:
            json_message = {
                "msg_type": mess_type,
                "sender": session_data.username,
                "string_data": string_message,
                "session_id": session_data.session_id,
                "sequence_number": sequence_num,
                "packet": 25
            }
            cmd_message = command_message.objects.create(
                current_date=current_date,
                current_time=current_time,
                terminal_id=terminal_id,
                command_code=command_code,
                query_message=query_message,
                data=string_message,
                sequence_num=sequence_num,
                json_data=json_message,
                send_by=request.user
            )
            try:
              async_to_sync(send_message_to_natsat)(json_message)
            except Exception as e:
                print(e)
            return redirect("/message/send-command/")
        else:
            wss_fail = True
    return render(request, "messages/send-command.html", locals())



@login_required(login_url="/login/")
def send_reboot_message(request):
    if request.method == "POST":
        mess_type = 62
        terminal_id = request.POST['terminal_id']
        reboot_code = request.POST['reboot-code']
        current_data = datetime.now()
        current_date = datetime.strftime(current_data, "%d%m%y")
        current_time = datetime.strftime(current_data, "%H%M")
        string_message = f"#@{mess_type}{current_date}{current_time}{terminal_id}{reboot_code}@#"
        session_data = ws_sessions.objects.last()
        sequence_num = reboot_sequence_generator()
        if session_data.logout is False:
            json_message = {
                "msg_type": mess_type,
                "sender": session_data.username,
                "string_data": string_message,
                "session_id": session_data.session_id,
                "sequence_number": sequence_num,
                "packet": 25
            }
            reboot_message.objects.create(
                current_date=current_date,
                current_time=current_time,
                terminal_id=terminal_id,
                reboot_code=reboot_code,
                json_data=json_message,
                sequence_num=sequence_num,
                send_by=request.user
            )
            try:
              async_to_sync(send_message_to_natsat)(json_message)
            except Exception as e:
                print(e)
            return redirect("/message/send-reboot/")
        else:
            wss_fail = True

    return render(request, "messages/reboot-message.html", locals())


@login_required(login_url="/login/")
def send_weather_forecast(request):
    weather_codes = weather_forecast_code.objects.all()
    if request.method == 'POST':
        start_date = request.POST['start-date']
        grid_id = request.POST['grid-id']
        num_of_forecast_day = request.POST['num-of-forecast-day']
        forecast_area = request.POST['forecast-area']
        day_1 = request.POST.get('day-1')
        if day_1 is None:
            day_1=0
        day_2 = request.POST.get('day-2')
        if day_2 is None:
            day_2=0
        day_3 = request.POST.get('day-3')
        if day_3 is None:
            day_3=0
        day_4 = request.POST.get('day-4')
        if day_4 is None:
            day_4=0
        day_5 = request.POST.get('day-5')
        if day_5 is None:
            day_5=0
        day_6 = request.POST.get('day-6')
        if day_6 is None:
            day_6=0
        current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        format_date = datetime.strftime(current_date, "%d%m%y")
        weather_forecast(request.user, format_date, grid_id, num_of_forecast_day, forecast_area, day_1, day_2, day_3, day_4, day_5, day_6)
        return redirect("/message/send-weather-forecast/")
    return render(request, "messages/send-weather-forecast.html", locals())


@login_required(login_url="/login/")
def show_send_weather(request):
    if request.method == "POST":
        date = request.POST['search-date']
        return redirect(f"/message/show-send-weather-messages/?q={date}")
    if request.GET.get("q"):
        date = request.GET.get("q")
        messages = Weather_Forecast_Message.objects.filter(send_on__date=date)
    else:
       messages = Weather_Forecast_Message.objects.all()[:100]
    return render(request, "messages/show-send-weather.html", locals())

@login_required(login_url="/login/")
def message_backup_info(request):
    datas = message_backup.objects.all()[:50]
    if request.method == "POST":
        date = request.POST['search-date']
        datas = message_backup.objects.filter(date=date)
        messages = Receive_message.objects.filter(received_on__date=date)
    return render(request, "dashboard/message-backup.html", locals())


@login_required(login_url="/login/")
def send_critical_alert(request):
    if request.method == "POST":
        start_date = request.POST['start_date']
        grid_id = request.POST['grid_id']
        alert_valid = request.POST['alert_valid']
        avalanche_axis_id = request.POST['avalanche_axis_id']
        alert_message = request.POST['alert_message']
        current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        format_date = datetime.strftime(current_date, "%d%m%y")
        critical_alert(request.user,
                       start_date=format_date,
                       grid_id=grid_id,
                       num_of_day=alert_valid,
                       avalanche_axis_id=avalanche_axis_id,
                       alert_message=alert_message,
                       )
    return render(request, "messages/send-critical-message.html", locals())

from django.db.models import Q
@login_required(login_url='/login/')
def show_critical_messages(request):
    s_time = request.GET.get("search-time")
    date = request.GET.get("search-date")
    if date and s_time:
        print(s_time)
        messages = site_critical_alert.objects.filter(send_on__date=date,send_on__time=s_time)
    elif date:
        date = date
        messages = site_critical_alert.objects.filter(send_on__date=date)
    else:
        date = datetime.now().date()
        messages = site_critical_alert.objects.filter(send_on__date=date)
    return render(request, "messages/show-critical-message.html", locals())



@login_required(login_url="/login/")
def avalanche_axis_update(request):

    return render(request, "messages/avalanche-axis-update.html", locals())


@login_required(login_url="/login/")
def avalanche_code_update(request):
    return render(request, "messages/avalanche-code-update.html", locals())


@login_required(login_url="/login/")
def weather_area_update(request):

    return render(request, "messages/weather-area-update.html", locals())


@login_required(login_url="/login/")
def weather_code_update(request):

    return render(request, "messages/weather-code-update.html", locals())
