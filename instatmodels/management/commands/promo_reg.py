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


def promo_last_reg_step(message, phone_number, name_promo, surname_promo,
                        second_name_promo, birth_date_promo, promo_city, promo_description):
    end_reg = telebot.types.ReplyKeyboardMarkup()
    end_reg.row('Завершить регистрацию', 'Start')
    promo_user_id = message.from_user.id
    phone_number = phone_number
    promo_id = encode_id(phone_number)
    name_promo = name_promo
    surname_promo = surname_promo
    second_name_promo = second_name_promo
    birth_date_promo = birth_date_promo
    age = age_calculate(birth_date_promo)
    promo_city = promo_city
    promo_description = promo_description
    bot.send_message(message.chat.id, f'ID пользователя в Telegram: {promo_user_id}\n'
                                      f'Введенный номер телефона: {phone_number}\n'
                                      f'Уникальный ID сотрудника для проекта: {promo_id}\n'
                                      f'Имя: {name_promo}\n'
                                      f'Фамилия: {surname_promo}\n'
                                      f'Отчество: {second_name_promo}\n'
                                      f'Дата рождения: {birth_date_promo}\n'
                                      f'Возраст: {age}\n'
                                      f'Город: {promo_city}\n'
                                      f'О себе: {promo_description}')
    bot.send_message(message.chat.id, 'Если данные введены вверно нажмите -Завершить регистрацию-.\n\n'
                                      'Если данные введены неверно, то нажмите -Start-, чтобы начать процесс'
                                      ' регистрации заново', reply_markup=end_reg)
    bot.register_next_step_handler(message, promo_save_after_reg, phone_number, name_promo, surname_promo,
                                   second_name_promo, birth_date_promo, promo_city, promo_description)


def enter_promo_description(message, phone_number, name_promo, surname_promo,
                            second_name_promo, birth_date_promo, promo_city):
    promo_description = message.text
    bot.send_message(message.chat.id, 'Все данные введены корректно\n\n'
                                      'Давайте все еще раз проверим')
    promo_last_reg_step(message, phone_number, name_promo, surname_promo, second_name_promo, birth_date_promo,
                        promo_city, promo_description)


def enter_promo_city(message, phone_number, name_promo, surname_promo, second_name_promo, birth_date_promo):
    check = word_lang_check(message.text)
    if check == 1:
        promo_city = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Город введён корректно\n\n'
                                          'Введите информацию о себе в произвольном формате')
        bot.register_next_step_handler(message, enter_promo_description, phone_number, name_promo, surname_promo,
                                       second_name_promo, birth_date_promo, promo_city)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_promo_city, phone_number, name_promo, surname_promo,
                                       second_name_promo, birth_date_promo)


def enter_birth_date_promo(message, phone_number, name_promo, surname_promo, second_name_promo):
    check = birth_date_check(message.text)
    if check == 1:
        birth_date_promo = message.text
        bot.send_message(message.chat.id, 'Дата рождения введена корректно\n\n'
                                          'Введите город, в котором планируете работать')
        bot.register_next_step_handler(message, enter_promo_city, phone_number, name_promo, surname_promo,
                                       second_name_promo, birth_date_promo)
    elif check == 0:
        bot.send_message(message.chat.id, 'Введите дату рождения в формате ДЕНЬ.МЕСЯЦ.ГОД')
        bot.register_next_step_handler(message, enter_birth_date_promo, phone_number, name_promo, surname_promo,
                                       second_name_promo)


def enter_second_name_promo(message, phone_number, name_promo, surname_promo):
    check = word_lang_check(message.text)
    if check == 1:
        second_name_promo = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Отчество введено корректно\n\n'
                                          'Введите вашу дату рождения в формате 4.11.1994')
        bot.register_next_step_handler(message, enter_birth_date_promo, phone_number, name_promo, surname_promo,
                                       second_name_promo)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_second_name_promo, phone_number, name_promo, surname_promo)


def enter_surname_promo(message, phone_number, name_promo):
    check = word_lang_check(message.text)
    if check == 1:
        surname_promo = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Фамилия введена корректно\n\n'
                                          'Введите ваше отчество на русском языке')
        bot.register_next_step_handler(message, enter_second_name_promo, phone_number, name_promo, surname_promo)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_surname_promo, phone_number, name_promo)


def enter_name_promo(message, phone_number):
    check = word_lang_check(message.text)
    if check == 1:
        name_promo = correct_entry(message.text).capitalize()
        bot.send_message(message.chat.id, 'Имя введено корректно\n\n'
                                          'Введите вашу фамилию на русском языке')
        bot.register_next_step_handler(message, enter_surname_promo, phone_number, name_promo)
    elif check == 2:
        bot.send_message(message.chat.id, 'Введите текст повторно на русском языке')
        bot.register_next_step_handler(message, enter_name_promo, phone_number)


def enter_number_promo(message):
    check = phone_check(message.text)
    if check == 1:
        phone_number = correct_entry(message.text)
        bot.send_message(message.chat.id, 'Номер телефона введен корректно\n\n'
                                          'Введите ваше полное имя на русском языке')
        bot.register_next_step_handler(message, enter_name_promo, phone_number)
    elif check == 2:
        bot.send_message(message.chat.id, f'Вы ввели меньше цифр, чем нужно\n\nПовторите ввод')
        bot.register_next_step_handler(message, enter_number_promo)
    elif check == 3:
        bot.send_message(message.chat.id, f'Неверный формат номера телефона\nНеоходимо ввести номер в формате'
                                          f' +79991112233\n\nПовторите ввод')
        bot.register_next_step_handler(message, enter_number_promo)


def promo_save_after_reg(message, phone_number, name_promo, surname_promo,
                         second_name_promo, birth_date_promo, promo_city, promo_description):
    if message.text == 'Завершить регистрацию':
        new_commands = telebot.types.ReplyKeyboardMarkup()
        new_commands.row('Публикация вакансии', 'Запросить список активных проектов',
                         'Заполнить дополнительную информацию о себе')
        promo = ProfilePromo(
            phone_number=phone_number,
            real_name=name_promo,
            real_surname=surname_promo,
            real_secondName=second_name_promo,
            birth_date=birth_date_promo,
            city=promo_city,
            description=promo_description,
            promo_unique_id=encode_id(phone_number),
            promo_telegram_id=message.from_user.id,
            promo_telegram_username=message.from_user.username,
        )
        promo.save()
        bot.send_message(message.chat.id, 'Вы только что закончили регистрацию, новые команды к вашим услугам',
                         reply_markup=new_commands)
    else:
        promo_first_step_reg(message)


def promo_first_step_reg(message):
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите ваш номер телефона', reply_markup=hideBoard)
    bot.register_next_step_handler(message, enter_number_promo)
