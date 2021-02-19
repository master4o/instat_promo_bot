import datetime as dt


def what_time_django():
    django_time = dt.datetime.utcnow() + dt.timedelta(hours=3)
    now = django_time.strftime('%d.%m.%Y - %H:%M:%S')
    return now


def time_convert(unix_time, time_format=None):
    converted_time = dt.datetime.fromtimestamp(unix_time) + dt.timedelta(hours=3)
    if time_format is None:
        return converted_time.strftime('%Y.%m.%d - %H:%M:%S')
    elif time_format == 'hour':
        return converted_time.strftime('%H')
    elif time_format == 'day':
        return converted_time.strftime('%d')
    elif time_format == 'month':
        return converted_time.strftime('%m')


pub_date = '21.01.2021 - 14:08:00'

now = what_time_django()

now = dt.datetime.strptime(now, '%d.%m.%Y - %H:%M:%S')
pub_date = dt.datetime.strptime(pub_date, '%d.%m.%Y - %H:%M:%S')

diff = now - pub_date
print(time_convert(pub_date))
