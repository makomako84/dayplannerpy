from  datetime import  datetime


def serialize_datetime(datetime:datetime):
    if isinstance(datetime, datetime):
        return "{}-{}-{} {}:{}".format(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute)

def deserialize_datetime(datetimestr:str) -> datetime:
    return datetime.strptime(datetimestr, '%Y-%m-%d %H:%M')
