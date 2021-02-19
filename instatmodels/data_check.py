import datetime as dt
import re


def phone_check(phone_number):
    check_phone_number = re.match(r'[+]{1}[7]{1}[0-9]{10}', phone_number)
    if check_phone_number and len(phone_number) == 12:
        return 1
    elif len(phone_number) < 12:
        return 2
    elif not check_phone_number:
        return 3


def word_lang_check(word):
    check_word_lang = re.search('[a-zA-Z0-9]{1,}', word)

    if check_word_lang is None:
        return 1
    else:
        return 2


def correct_entry(entry):
    return re.sub('\s+', '', entry)


def birth_date_check(birth_date):
    try:
        birth_date = dt.datetime.strptime(birth_date, '%d.%m.%Y')
        return 1
    except ValueError:
        return 0


def true_check(bool):
    if bool:
        return 'Да'
    else:
        return 'Нет'


def digit_check(digit):
    try:
        int(digit)
        return 1
    except ValueError:
        return 0


def project_status_check(start_date, end_date):
    date_format = '%d.%m.%Y'
    start_date = dt.datetime.strptime(start_date, date_format)
    end_date = dt.datetime.strptime(end_date, date_format)
    now = dt.datetime.today()
    if start_date <= now <= end_date:
        return 'Проект активен'
    elif now > end_date:
        return 'Проект закончен'
    elif now < start_date:
        return 'Проект еще не начался'
