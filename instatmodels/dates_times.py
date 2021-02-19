import datetime as dt

from dateutil.parser import parse as du_parse
from dateutil.relativedelta import relativedelta

UTC_OFFSET = {
    'Москва': 3,
    'Санкт-Петербург': 3,
    'Новосибирск': 7,
    'Екатеринбург': 5,
    'Нижний Новгород': 3,
    'Казань': 3,
    'Челябинск': 5,
    'Омск': 6,
    'Самара': 4,
    'Ростов-на-Дону': 3,
    'Уфа': 5,
    'Красноярск': 7,
    'Воронеж': 3,
    'Пермь': 5,
    'Волгоград': 4,
    'Краснодар': 3,
    'Калининград': 2,
    'Владивосток': 10
}


def what_time_django():
    django_time = dt.datetime.utcnow() + dt.timedelta(hours=3)
    now = django_time.strftime('%d.%m.%Y - %H:%M:%S')
    return now


def what_time(city):
    city = str.capitalize(city)
    return what_time_general(city)


def what_time_general(city):
    offset = UTC_OFFSET[city]
    city_time = dt.datetime.utcnow() + dt.timedelta(hours=offset)
    f_time = city_time.strftime('%H:%M')
    return f_time


def day_time_no_city():
    current_hour = dt.datetime.utcnow() + dt.timedelta(hours=3)
    if int(current_hour.strftime('%H')) < 6:
        text = 'Доброй ночи!'
    elif int(current_hour.strftime('%H')) < 11:
        text = 'Доброе утро!'
    elif int(current_hour.strftime('%H')) < 18:
        text = 'Добрый день!'
    elif int(current_hour.strftime('%H')) < 23:
        text = 'Добрый вечер!'
    else:
        text = 'Доброй ночи!'
    return text


def day_time_city(city):
    offset = UTC_OFFSET[city]
    current_hour = dt.datetime.utcnow() + dt.timedelta(hours=offset)
    if int(current_hour.strftime('%H')) < 6:
        text = 'Доброй ночи!'
    elif int(current_hour.strftime('%H')) < 11:
        text = 'Доброе утро!'
    elif int(current_hour.strftime('%H')) < 18:
        text = 'Добрый день!'
    elif int(current_hour.strftime('%H')) < 23:
        text = 'Добрый вечер!'
    else:
        text = 'Доброй ночи!'
    return text


def time_convert(unix_time, time_format=None):
    converted_time = dt.datetime.fromtimestamp(unix_time) + dt.timedelta(hours=3)
    if time_format is None:
        return converted_time.strftime('%d.%m.%Y - %H:%M:%S')
    elif time_format == 'hour':
        return converted_time.strftime('%H')
    elif time_format == 'day':
        return converted_time.strftime('%d')
    elif time_format == 'month':
        return converted_time.strftime('%m')


def age_calculate(birth_date):
    date_format = '%d.%m.%Y'
    corrected_entering_date = (dt.datetime.strptime(birth_date, date_format)).date()
    current_hour = (dt.datetime.utcnow() + dt.timedelta(hours=3)).date()
    age = relativedelta(du_parse(str(current_hour)), du_parse(str(corrected_entering_date)))
    return age.years


def verified_status_text(verified_status):
    if verified_status:
        return f'Аккаунт подтвержден'
    else:
        return f'Аккаунт еще не подтвержден'


def date_diff_agency(agency):
    now_time = what_time_django()
    pub_time = time_convert(int(agency.last_pub))
    now_time = dt.datetime.strptime(now_time, '%d.%m.%Y - %H:%M:%S')
    pub_time = dt.datetime.strptime(pub_time, '%d.%m.%Y - %H:%M:%S')
    diff = now_time - pub_time
    return diff.seconds


def date_diff_project(project):
    now_time = what_time_django()
    pub_time = time_convert(int(project.pub_date))
    now_time = dt.datetime.strptime(now_time, '%d.%m.%Y - %H:%M:%S')
    pub_time = dt.datetime.strptime(pub_time, '%d.%m.%Y - %H:%M:%S')
    diff = now_time - pub_time
    return diff.days
