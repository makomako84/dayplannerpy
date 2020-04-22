from  datetime import  datetime


def serializeDate(date):
    if isinstance(date, datetime):
        return "{}-{}-{} {}:{}".format(date.year, date.month, date.day, date.hour, date.minute)

def deserializeDate(datestr):
    return datetime.strptime(datestr, '%Y-%m-%d %H:%M')
