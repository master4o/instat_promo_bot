import telebot
from telebot import types

from ...dates_times import day_time_no_city
from ...models import ProfilePromo, bot
from .edit_promo import edit_promo
from .rate_reg import agency_rate_reg
from .request_reg import request_reg
from .Review_reg import agency_review_reg


def show_requests(message):
    hideBoard = types.ReplyKeyboardRemove()
    if message.text == 'Подтвержденные отклики':
        promo = ProfilePromo.objects.get(promo_telegram_id=message.from_user_id)
        requests = promo.promo_requests.all()
        for req in requests:
            if req.accept_status:
                bot.send_message(message.chat.id, f'{req}', reply_markup=hideBoard)

    elif message.text == 'Неподтвержденные отклики':
        promo = ProfilePromo.objects.get(promo_telegram_id=message.from_user_id)
        requests = promo.promo_requests.all()
        for req in requests:
            if not req.accept_status:
                bot.send_message(message.chat.id, f'{req}', reply_markup=hideBoard)


def enter_project_name_for_request(message):
    request_reg(message)


def promo_menu_choose(message):
    hideBoard = types.ReplyKeyboardRemove()
    promo_menu_bar = telebot.types.ReplyKeyboardMarkup()
    promo_menu_bar.row('Показать статус откликов', 'Откликнуться на вакансию')
    promo_menu_bar.row('Покажи мою личную анкету', 'Изменить свою анкету')
    promo_menu_bar.row('Оставить отзыв об агентстве', 'Оценить агентство')
    request_list = telebot.types.ReplyKeyboardMarkup()
    request_list.row('Подтвержденные отклики', 'Неподтвержденные отклики')
    choice_for_edit = telebot.types.ReplyKeyboardMarkup()
    choice_for_edit.row('Добавить', 'Изменить')
    if message.text == 'Показать статус откликов':
        bot.send_message(message.chat.id, 'Могу показать список ваших откликов за последний месяц, '
                                          'выберите тип откликов из меню', reply_markup=request_list)
        bot.register_next_step_handler(message, show_requests)
    elif message.text == 'Откликнуться на вакансию':
        bot.send_message(message.chat.id, 'Введите название проекта из вакансии, убрав ковычки', reply_markup=hideBoard)
        bot.register_next_step_handler(message, enter_project_name_for_request)
    elif message.text == 'Покажи мою личную анкету':
        promo = ProfilePromo.objects.get(promo_telegram_id=message.from_user.id)
        bot.send_message(message.chat.id, f'Ваша анкета:\n'
                                          f'{promo}', reply_markup=hideBoard)
    elif message.text == 'Изменить свою анкету':
        bot.send_message(message.chat.id, 'Хотите добавить или изменить данные?', reply_markup=choice_for_edit)
        edit_promo(message)
    elif message.text == 'Оставить отзыв об агентстве':
        agency_review_reg(message)
    elif message.text == 'Оценить агентство':
        agency_rate_reg(message)
    else:
        promo = ProfilePromo.objects.get(promo_telegram_id=message.from_user.id)
        bot.send_message(message.chat.id, f'{promo.real_name}, \n\n'
                                          f'Для начала работы, выберите пункт меню', reply_markup=promo_menu_bar)
        bot.register_next_step_handler(message, promo_menu_choose)


def promo_menu(message):
    promo_menu_bar = telebot.types.ReplyKeyboardMarkup()
    promo_menu_bar.row('Показать статус откликов', 'Откликнуться на вакансию')
    promo_menu_bar.row('Покажи мою личную анкету', 'Изменить свою анкету')
    promo_menu_bar.row('Оставить отзыв об агентстве', 'Оценить агентство')
    hello_message = day_time_no_city()
    promo = ProfilePromo.objects.get(promo_telegram_id=message.from_user.id)
    bot.send_message(message.chat.id, f'{promo.real_name}, {hello_message}\n\n'
                                      f'Для начала работы, выберите пункт меню', reply_markup=promo_menu_bar)
    bot.register_next_step_handler(message, promo_menu_choose)
