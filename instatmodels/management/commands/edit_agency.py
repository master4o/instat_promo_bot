import telebot
from telebot import types

from ...data_check import birth_date_check, phone_check
from ...models import ProfileAgency, ProfilePromo, bot

hideBoard = types.ReplyKeyboardRemove()


def edit_agency_photo(message, agency):
    pass


def edit_promo_vacancy_photo(message, agency):
    pass


def edit_sv_vacancy_photo(message, agency):
    pass


def edit_helper_vacancy_photo(message, agency):
    pass


def edit_other_vacancy_photo(message, agency):
    pass


def edit_description(message, agency):
    agency.description = message.text
    agency.save()
    bot.send_message(message.chat.id, f'Ваше описание в анкете:\n{agency.description}\n'
                                      f'Введите /start, чтобы продолжить')


def edit_city(message, agency):
    city = message.text.capitalize()
    agency.city = city
    agency.save()
    bot.send_message(message.chat.id, f'Теперь ваш город - {agency.city}\n'
                                      f'Введите /start, чтобы продолжить')


def edit_agency_phone_number(message, agency):
    phone = message.text
    check = phone_check(phone)
    if check == 1:
        agency.agency_phone_number = phone
        agency.save()
        bot.send_message(message.chat.id, f'Ваш номер телефона теперь - {agency.agency_phone_number}\n'
                                          f'Введите /start, чтобы продолжить')
    elif check == 2:
        bot.send_message(message.chat.id, f'Вы ввели меньше цифр, чем нужно\n\nПовторите ввод')
        bot.register_next_step_handler(message, edit_phone, agency)
    elif check == 3:
        bot.send_message(message.chat.id, f'Неверный формат номера телефона\nНеоходимо ввести номер в формате'
                                          f' +79991112233\n\nПовторите ввод')
        bot.register_next_step_handler(message, edit_phone, agency)
    else:
        bot.send_message(message.chat.id, 'Введите /start, чтобы продолжить')


def edit_phone(message, agency):
    phone = message.text
    check = phone_check(phone)
    if check == 1:
        agency.phone_number = phone
        agency.save()
        bot.send_message(message.chat.id, f'Ваш номер телефона теперь - {agency.phone_number}\n'
                                          f'Введите /start, чтобы продолжить')
    elif check == 2:
        bot.send_message(message.chat.id, f'Вы ввели меньше цифр, чем нужно\n\nПовторите ввод')
        bot.register_next_step_handler(message, edit_phone, agency)
    elif check == 3:
        bot.send_message(message.chat.id, f'Неверный формат номера телефона\nНеоходимо ввести номер в формате'
                                          f' +79991112233\n\nПовторите ввод')
        bot.register_next_step_handler(message, edit_phone, agency)
    else:
        bot.send_message(message.chat.id, 'Введите /start, чтобы продолжить')


def edit_agency_name(message, agency):
    agency_name = message.text.capitalize()
    agency.agency_name = agency_name
    agency.save()
    bot.send_message(message.chat.id, f'Название агентства теперь - "{agency.agency_name}"\n'
                                      f'Введите /start, чтобы продолжить')


def edit_surname(message, agency):
    surname = message.text.capitalize()
    agency.real_surname = surname
    agency.save()
    bot.send_message(message.chat.id, f'Ваша фамилия теперь - {agency.real_surname}\nВведите /start, чтобы продолжить')


def edit_name(message, agency):
    name = message.text.capitalize()
    agency.real_name = name
    agency.save()
    bot.send_message(message.chat.id, f'Ваше имя теперь - {agency.real_name}\nВведите /start, чтобы продолжить')


def edit_bar(message):
    agency = ProfileAgency.objects.get(agency_telegram_id=message.from_user.id)
    if message.text == 'Имя':
        name = agency.real_name
        bot.send_message(message.chat.id, f'Ваше текущее имя {name}, введите повторно Ваше настоящее имя для '
                                          f'изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_name, agency)
    elif message.text == 'Фамилия':
        surname = agency.real_surname
        bot.send_message(message.chat.id, f'Ваше текущее имя {surname}, введите повторно Ваше настоящее имя для '
                                          f'изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_surname, agency)
    elif message.text == 'Название агентства':
        agency_name = agency.agency_name
        bot.send_message(message.chat.id, f'Текущее название агентства в анкете - {agency_name}, '
                                          f'введите повторно название агентства для '
                                          f'изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_agency_name, agency)
    elif message.text == 'Телефон':
        phone = agency.phone_number
        bot.send_message(message.chat.id, f'Ваше текущий номер телефона - {phone}, введите повторно ваш номер телефона'
                                          f' для изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_phone, agency)
    elif message.text == 'Телефон агентства':
        phone = agency.agency_phone_number
        bot.send_message(message.chat.id, f'Текущий номер телефона агентства - {phone}, '
                                          f'введите повторно ваш номер телефона'
                                          f' для изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_agency_phone_number, agency)
    elif message.text == 'Город':
        city = agency.city
        bot.send_message(message.chat.id, f'Ваш текущий город - {city}', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_city, agency)
    elif message.text == 'Описание':
        description = agency.description
        bot.send_message(message.chat.id, f'Ваше текущее описание:\n{description}\nВведите новое описание для анкеты')
        bot.register_next_step_handler(message, edit_description, agency)
    elif message.text == 'Фото представителя':
        pass
        # img = open('.../static/promo_telegram_id/unface.jpg')
        # bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        # bot.register_next_step_handler(message, edit_agency_photo, agency)
    elif message.text == 'Фото Промо':
        pass
        # img = open('.../static/promo_telegram_id/full.jpg')
        # bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        # bot.register_next_step_handler(message, edit_promo_vacancy_photo, agency)
    elif message.text == 'Фото СВ':
        pass
        # img = open('.../static/promo_telegram_id/photo_1.jpg')
        # bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        # bot.register_next_step_handler(message, edit_sv_vacancy_photo, agency)
    elif message.text == 'Фото Хелпер':
        pass
        # img = open('.../static/promo_telegram_id/photo_2.jpg')
        # bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        # bot.register_next_step_handler(message, edit_helper_vacancy_photo, agency)
    elif message.text == 'Фото Другое':
        pass
        # img = open('.../static/promo_telegram_id/photo_3.jpg')
        # bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        # bot.register_next_step_handler(message, edit_other_vacancy_photo, agency)
    else:
        bot.send_message(message.chat.id, f'Введите /start, чтобы продолжить')


def add_bar(message):
    if message.text == 'Фото представителя':
        pass
    elif message.text == 'Фото Промо':
        pass
    elif message.text == 'Фото СВ':
        pass
    elif message.text == 'Фото Хелпер':
        pass
    elif message.text == 'Фото Другое':
        pass
    else:
        pass


def make_choice(message):
    agency_edit_bar = telebot.types.ReplyKeyboardMarkup()
    agency_edit_bar.row('Имя', 'Фамилия', 'Название агентства')
    agency_edit_bar.row('Телефон', 'Телефон агентства', 'Город')
    agency_edit_bar.row('Описание')
    agency_edit_bar.row('Фото представителя', 'Фото Промо')
    agency_edit_bar.row('Фото СВ', 'Фото Хелпер', 'Фото Другое')
    agency_add_bar = telebot.types.ReplyKeyboardMarkup()
    agency_add_bar.row('Фото представителя', 'Фото Промо')
    agency_add_bar.row('Фото СВ', 'Фото Хелпер', 'Фото Другое')

    if message.text == 'Добавить':
        bot.send_message(message.chat.id, 'Выберите пункт анкеты для добавления', reply_markup=agency_add_bar)
        bot.register_next_step_handler(message, add_bar)
    elif message.text == 'Изменить':
        bot.send_message(message.chat.id, 'Выберите пункт анкеты для изменения', reply_markup=agency_edit_bar)
        bot.register_next_step_handler(message, edit_bar)


def edit_agency(message):
    agency_edit_bar = telebot.types.ReplyKeyboardMarkup()
    agency_edit_bar.row('Добавить', 'Изменить')
    bot.send_message(message.chat.id, 'Выберите, что хотите сделать с вашими личными данными',
                     reply_markup=agency_edit_bar)
    bot.register_next_step_handler(message, make_choice)
