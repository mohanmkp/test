from wss_handler.models import Avalanche_message_one, ws_sessions
from datetime import datetime
from chatapp.views import send_message_to_natsat
from asgiref.sync import async_to_sync

def avalanche_sequence_generator():
    today_date = datetime.now().date()
    query = Avalanche_message_one.objects.filter(message_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1

    else:
        return 10



def avalanche_forecaster_message_one(
        user,
        start_date,
        grid_id,
        num_axis,
        axis_ids,
        forecast_codes,

):
    message_type = 91
    axis_id = {
        "axis1": '00', "axis2": '00', "axis3": '00', "axis4": '00', "axis5": '00', "axis6": '00', "axis7": '00',
        "axis8": '00', "axis9": '00', "axis10": '00', "axis11": '00', "axis12": '00', "axis13": '00', "axis14": '00', "axis15": '00',
    }
    forecast_code = {
        "forecast1": '0', "forecast2": '0', "forecast3": '0', "forecast4": '0', "forecast5": '0', "forecast6": '0', "forecast7": '0',
        "forecast8": '0', "forecast9": '0', "forecast10": '0', "forecast11": '0', "forecast12": '0', "forecast13": '0', "forecast14": '0',
        "forecast15": '0',
    }
    count = 1
    for i, j in zip(axis_ids, forecast_codes):
        axis_id[f'axis{count}'] = i
        forecast_code[f'forecast{count}'] = j
        count = count + 1

    packet = f"#@{message_type}{start_date}{grid_id}{num_axis}{axis_id['axis1']}{forecast_code['forecast1']}{axis_id['axis2']}{forecast_code['forecast2']}" \
             f"{axis_id['axis3']}{forecast_code['forecast3']}{axis_id['axis4']}{forecast_code['forecast4']}{axis_id['axis5']}{forecast_code['forecast5']}{axis_id['axis6']}{forecast_code['forecast6']}" \
             f"{axis_id['axis7']}{forecast_code['forecast7']}{axis_id['axis8']}{forecast_code['forecast8']}{axis_id['axis9']}{forecast_code['forecast9']}{axis_id['axis10']}{forecast_code['forecast10']}" \
             f"{axis_id['axis11']}{forecast_code['forecast11']}{axis_id['axis12']}{forecast_code['forecast12']}{axis_id['axis13']}{forecast_code['forecast13']}{axis_id['axis14']}{forecast_code['forecast14']}{axis_id['axis15']}{forecast_code['forecast15']}@#"
    session_data = ws_sessions.objects.last()
    sequence_num = avalanche_sequence_generator()

    message_json = {
        "msg_type": 92,
        "sender": session_data.username,
        "string_data": packet,
        "session_id": session_data.session_id,
        "sequence_number": sequence_num,
        "packet": 1
    }
    message1 = Avalanche_message_one.objects.create(
        packet=packet,
        message_type=message_type,
        start_date=start_date,
        grid_id=grid_id,
        num_of_axis=num_axis,
        axis_ids=axis_id,
        forecast_codes=forecast_code,
        sequence_num=sequence_num,
        data=message_json,
        sender_user=user
    )

    try:
        async_to_sync(send_message_to_natsat)(message_json)
    except Exception as e:
        print(e)
    return message1

def avalanche_forecaster_message_two(
        message_one,
        start_date,
        grid_id,
        outlook
):
    message_type = 98
    message_encode = f"#@{start_date}{grid_id}{outlook}@#"


