import telebot
from telebot import types

from ...data_check import birth_date_check, phone_check
from ...models import ProfileAgency, ProfilePromo, bot

hideBoard = types.ReplyKeyboardRemove()


def edit_photo_3(message, promo):
    pass


def edit_photo_2(message, promo):
    pass


def edit_photo_1(message, promo):
    pass


def edit_full_photo(message, promo):
    pass


def edit_unface(message, promo):
    pass


def edit_promo_description(message, promo):
    description = promo.description
    promo.description = description
    promo.save()
    bot.send_message(message.chat.id, f'Новое описание в вашецй анкете:\n{description}\nВведите /start, чтобы '
                                      f'продолжить')


def edit_city(message, promo):
    city = message.text.capitalize()
    promo.city = city
    promo.save()
    bot.send_message(message.chat.id, f'Теперь ваш город - {promo.city}\n'
                                      f'Введите /start, чтобы продолжить')


def edit_birth_date(message, promo):
    birth_date = message.text
    check = birth_date_check(message.text)
    if check == 1:
        promo.birth_date = birth_date
        promo.save()
        bot.send_message(message.chat.id, f'Теперь ваша дата рождения - {promo.birth_date}\n'
                                          f'Введите /start, чтобы продолжить')
    elif check == 0:
        bot.send_message(message.chat.id, 'Введите дату рождения в формате ДЕНЬ.МЕСЯЦ.ГОД')
        bot.register_next_step_handler(message, edit_birth_date, promo)


def edit_phone(message, promo):
    phone = message.text
    check = phone_check(phone)
    if check == 1:
        promo.phone_number = phone
        promo.save()
        bot.send_message(message.chat.id, f'Ваш номер телефона теперь - {promo.phone_number}\n '
                                          f'Введите /start, чтобы продолжить')
    elif check == 2:
        bot.send_message(message.chat.id, f'Вы ввели меньше цифр, чем нужно\n\nПовторите ввод')
        bot.register_next_step_handler(message, edit_phone, promo)
    elif check == 3:
        bot.send_message(message.chat.id, f'Неверный формат номера телефона\nНеоходимо ввести номер в формате'
                                          f' +79991112233\n\nПовторите ввод')
        bot.register_next_step_handler(message, edit_phone, promo)
    else:
        bot.send_message(message.chat.id, 'Введите /start, чтобы продолжить')


def edit_second_name(message, promo):
    second_name = message.text.capitalize()
    promo.real_secondName = second_name
    promo.save()
    bot.send_message(message.chat.id, f'Ваше отчество теперь - {promo.real_secondName}\n '
                                      f'Введите /start, чтобы продолжить')


def edit_surname(message, promo):
    surname = message.text.capitalize()
    promo.real_surname = surname
    promo.save()
    bot.send_message(message.chat.id, f'Ваша фамилия теперь - {promo.real_surname}\nВведите /start, чтобы продолжить')


def edit_name(message, promo):
    name = message.text.capitalize()
    promo.real_name = name
    promo.save()
    bot.send_message(message.chat.id, f'Ваше имя теперь - {promo.real_name}\nВведите /start, чтобы продолжить')


def edit_bar(message):
    promo = ProfilePromo.objects.get(promo_telegram_id=message.from_user.id)
    if message.text == 'Имя':
        name = promo.real_name
        bot.send_message(message.chat.id, f'Ваше текущее имя {name}, введите повторно Ваше настоящее имя для '
                                          f'изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_name, promo)
    elif message.text == 'Фамилия':
        surname = promo.real_surname
        bot.send_message(message.chat.id, f'Ваше текущее имя {surname}, введите повторно Ваше настоящее имя для '
                                          f'изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_surname, promo)
    elif message.text == 'Отчество':
        second_name = promo.real_secondName
        bot.send_message(message.chat.id, f'Ваше текущее имя {second_name}, введите повторно Ваше настоящее имя для '
                                          f'изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_second_name, promo)
    elif message.text == 'Телефон':
        phone = promo.phone_number
        bot.send_message(message.chat.id, f'Ваше текущий номер телефона - {phone}, введите повторно ваш номер телефона'
                                          f' для изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_phone, promo)
    elif message.text == 'Дата рождения':
        birth_date = promo.birth_date
        bot.send_message(message.chat.id, f'Ваша текущая дата рождения {birth_date}, '
                                          f'введите новую дату рождения для '
                                          f'изменения в анкете', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_birth_date, promo)
    elif message.text == 'Город':
        city = promo.city
        bot.send_message(message.chat.id, f'Ваш текущий город - {city}', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_city, promo)
    elif message.text == 'Фото лица':
        img = open('.../static/promo_telegram_id/unface.jpg')
        bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_unface, promo)
    elif message.text == 'Фото полный рост':
        img = open('.../static/promo_telegram_id/full.jpg')
        bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_full_photo, promo)
    elif message.text == 'Фото_1':
        img = open('.../static/promo_telegram_id/photo_1.jpg')
        bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_photo_1, promo)
    elif message.text == 'Фото_2':
        img = open('.../static/promo_telegram_id/photo_2.jpg')
        bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_photo_2, promo)
    elif message.text == 'Фото_3':
        img = open('.../static/promo_telegram_id/photo_3.jpg')
        bot.send_photo(message.chat.id, img, reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_photo_3, promo)
    elif message.text == 'Описание':
        description = promo.description
        bot.send_message(message.chat.id, f'Ваше текущее описание:\n{description}\nВведите новое описание для '
                                          f'изменения анкеты', reply_markup=hideBoard)
        bot.register_next_step_handler(message, edit_promo_description, promo)
    else:
        bot.send_message(message.chat.id, f'Введите /start, чтобы продолжить')


def add_bar(message):
    if message.text == 'Фото полный рост':
        pass
    elif message.text == 'Фото лица':
        pass
    elif message.text == 'Фото_1':
        pass
    elif message.text == 'Фото_2':
        pass
    elif message.text == 'Фото_3':
        pass
    else:
        pass


def make_choice(message):
    promo_edit_bar = telebot.types.ReplyKeyboardMarkup()
    promo_edit_bar.row('Имя', 'Фамилия', 'Отчество')
    promo_edit_bar.row('Телефон', 'Дата рождения', 'Город')
    promo_edit_bar.row('Описание')
    promo_edit_bar.row('Фото лица', 'Фото полный рост')
    promo_edit_bar.row('Фото_1', 'Фото_2', 'Фото_3')
    promo_add_bar = telebot.types.ReplyKeyboardMarkup()
    promo_add_bar.row('Фото лица', 'Фото полный рост')
    promo_add_bar.row('Фото_1', 'Фото_2', 'Фото_3')

    if message.text == 'Добавить':
        bot.send_message(message.chat.id, 'Выберите пункт анкеты для добавления', reply_markup=promo_add_bar)
        bot.register_next_step_handler(message, add_bar)
    elif message.text == 'Изменить':
        bot.send_message(message.chat.id, 'Выберите пункт анкеты для изменения', reply_markup=promo_edit_bar)
        bot.register_next_step_handler(message, edit_bar)


def edit_promo(message):
    promo_edit_bar = telebot.types.ReplyKeyboardMarkup()
    promo_edit_bar.row('Добавить', 'Изменить')
    bot.send_message(message.chat.id, 'Выберите, что хотите сделать с вашими личными данными',
                     reply_markup=promo_edit_bar)
    bot.register_next_step_handler(message, make_choice)
