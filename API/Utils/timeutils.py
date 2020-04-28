from  datetime import  datetime as dt


def serialize_datetime(datetime:dt):
    if isinstance(datetime, dt):
        return "{}-{}-{} {}:{}".format(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute)

def deserialize_datetime(datetimestr:str) -> dt:
    return dt.strptime(datetimestr, '%Y-%m-%d %H:%M')
