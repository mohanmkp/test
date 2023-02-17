from wss_handler.models import Weather_Forecast_Message, ws_sessions
from chatapp.views import send_message_to_natsat
from asgiref.sync import async_to_sync
from datetime import datetime


def weather_sequence_generator():
    today_date = datetime.now().date()
    query = Weather_Forecast_Message.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1

    else:
        return 10



def weather_forecast(
         sender,
         start_date,
         grid_id,
         num_of_forecast_day,
         forecast_area,
         day_1=0,
         day_2=0,
         day_3=0,
         day_4=0,
         day_5=0,
         day_6=0
                ):
    message_encode = f"#@{start_date}{grid_id}{num_of_forecast_day}{forecast_area}{day_1}{day_2}{day_3}{day_4}{day_5}{day_6}@#"
    sequence_number = weather_sequence_generator()
    session_data = ws_sessions.objects.last()
    message_json = {
        "msg_type": 92,
        "sender": session_data.username,
        "string_data": message_encode,
        "session_id": session_data.session_id,
        "sequence_number": sequence_number,
        "packet": 2
    }

    Weather_Forecast_Message.objects.create(
        send_by=sender,
        json_data=message_json,
        sequence_num=sequence_number,
        start_date=start_date,
        grid_id=grid_id,
        num_of_forecast_day=num_of_forecast_day,
        forecast_area=forecast_area,
        day_1=day_1,
        day_2=day_2,
        day_3=day_3,
        day_4=day_4,
        day_5=day_5,
        day_6=day_6,
        packet=message_encode
    )

    try:
        async_to_sync(send_message_to_natsat)(message_json)
    except Exception as e:
        print(e)




