import telebot
from django.conf import settings
from telebot import types

from ...data_check import (birth_date_check, correct_entry, phone_check,
                           word_lang_check)
from ...dates_times import (age_calculate, day_time_city, day_time_no_city,
                            time_convert, what_time, what_time_general)
from ...encodeID import encode_id
from ...models import (ProfileAgency, ProfilePromo, Project, PromoRequest,
                       RateAgency, RatePromo, ReviewAgency, ReviewPromo, bot)


def agency_last_reg_step(message, phone_number, name_agency, surname_agency,
                         second_name_agency, agency_city, agency_description):
    end_reg = telebot.types.ReplyKeyboardMarkup()
    end_reg.row('Завершить регистрацию', 'Start')
    agency_user_id = message.from_user.id
    phone_number = phone_number
    agency_id = encode_id(phone_number)
    name_agency = name_agency
    surname_agency = surname_agency
    second_name_agency = second_name_agency
    agency_city = agency_city
    agency_description = agency_description
    bot.send_message(message.chat.id, f'ID пользователя в Telegram: {agency_user_id}\n'
                                      f'Введенный номер телефона: {phone_number}\n'
                                      f'Уникальный ID сотрудника для проекта: {agency_id}\n'
                                      f'Имя: {name_agency}\n'
                                      f'Фамилия: {surname_agency}\n'
                                      f'Название агентства: {second_name_agency}\n'
                                      f'Город: {agency_city}\n'
                                      f'О себе: {agency_description}')
    bot.send_message(message.chat.id, 'Если данные введены вверно нажмите -Завершить регистрацию-.\n\n'
                                      'Если данные введены неверно, то нажмите -Start-, чтобы начать процесс'
                                      ' регистрации заново', reply_markup=end_reg)
    bot.register_next_step_handler(message, agency_save_after_reg, phone_number, name_agency, surname_agency,
                                   second_name_agency, agency_city, agency_description)


def enter_agency_description(message, phone_number, name_agency, surname_agency,
                             second_name_agency, agency_city):
    agency_description = message.text
    bot.send_message(message.chat.id, 'Все данные введены корректно\n\n'
                                      'Давайте все еще раз проверим')
    agency_last_reg_step(message, phone_number, name_agency, surname_agency,
                         second_name_agency, agency_city, agency_description)


def enter_agency_city(message, phone_number, name_agency, surname_agency, second_name_agency, ):
    check = word_lang_check(message.text)
    if check == 1:
        agency_city = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Город введён корректно\n\n'
                                          'Введите информацию об Агентстве в произвольном формате')
        bot.register_next_step_handler(message, enter_agency_description, phone_number, name_agency, surname_agency,
                                       second_name_agency, agency_city)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_agency_city, phone_number, name_agency,
                                       surname_agency, second_name_agency, )


def enter_second_name_agency(message, phone_number, name_promo, surname_promo):
    check = word_lang_check(message.text)
    if check == 1:
        second_name_promo = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Название агентства введено корректно\n\n'
                                          'Введите город, в котором находится головной офис агентства')
        bot.register_next_step_handler(message, enter_agency_city, phone_number, name_promo, surname_promo,
                                       second_name_promo)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_second_name_agency, phone_number, name_promo, surname_promo)


def enter_surname_agency(message, phone_number, name_agency):
    check = word_lang_check(message.text)
    if check == 1:
        surname_agency = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Фамилия введена корректно\n\n'
                                          'Введите название Агентства на русском языке')
        bot.register_next_step_handler(message, enter_second_name_agency, phone_number, name_agency, surname_agency)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_surname_agency, phone_number, name_agency)


def enter_name_agency(message, phone_number):
    check = word_lang_check(message.text)
    if check == 1:
        name_agency = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Имя введено корректно\n\n'
                                          'Введите вашу фамилию на русском языке')
        bot.register_next_step_handler(message, enter_surname_agency, phone_number, name_agency)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_name_agency, phone_number)


def enter_number_agency(message):
    check = phone_check(message.text)
    if check == 1:
        phone_number = correct_entry(message.text)
        bot.send_message(message.chat.id, 'Номер телефона введен корректно\n\n'
                                          'Введите ваше полное имя на русском языке')
        bot.register_next_step_handler(message, enter_name_agency, phone_number)
    elif check == 2:
        bot.send_message(message.chat.id, f'Вы ввели меньше цифр, чем нужно\n\nПовторите ввод')
        bot.register_next_step_handler(message, enter_number_agency)
    elif check == 3:
        bot.send_message(message.chat.id, f'Неверный формат номера телефона\nНеоходимо ввести номер в формате'
                                          f' +79991112233\n\nПовторите ввод')
        bot.register_next_step_handler(message, enter_number_agency)


def agency_save_after_reg(message, phone_number, name_agency, surname_agency,
                          second_name_agency, agency_city, agency_description):
    if message.text == 'Завершить регистрацию':
        new_commands = telebot.types.ReplyKeyboardMarkup()
        new_commands.row('Публикация вакансии', 'Запросить список активных проектов',
                         'Заполнить дополнительную информацию о себе')
        agency = ProfileAgency(
            phone_number=phone_number,
            real_name=name_agency,
            real_surname=surname_agency,
            agency_name=second_name_agency,
            city=agency_city,
            description=agency_description,
            agency_unique_id=encode_id(phone_number),
            agency_telegram_id=message.from_user.id,
            agency_telegram_username=message.from_user.username,
        )
        agency.save()
        bot.send_message(message.chat.id, 'Вы только что закончили регистрацию, новые команды к вашим услугам',
                         reply_markup=new_commands)
    else:
        agency_first_step_reg(message)


def agency_first_step_reg(message):
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите ваш номер телефона', reply_markup=hideBoard)
    bot.register_next_step_handler(message, enter_number_agency)
