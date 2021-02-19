import telebot
from telebot import types

import datetime as dt

from ...dates_times import day_time_no_city, time_convert, what_time_django, date_diff_agency
from ...models import ProfileAgency, Project, bot, chat_id
from .edit_agency import edit_agency
from .edit_project import edit_project
from .project_reg import first_step_project_reg
from .rate_reg import promo_rate_reg
from .Review_reg import promo_review_reg


def project_repeat(message, agency):
    hideBoard = types.ReplyKeyboardRemove()
    p = Project.objects.filter(pk=message.text).exists()
    if p:
        diff = date_diff_agency(agency)
        if diff < 0:
            bot.send_message(message.chat.id, f'Опубликовать вакансию можно только раз в час. До повторной '
                                              f'публикации осталось {60 - (round((diff / 60), 0))} мин '
                                              f'{60 - (diff % 60)} сек', reply_markup=hideBoard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text='Откликнуться',
                                                         callback_data='request')
            keyboard.add(callback_button)
            p = Project.objects.filter(pk=message.text)[0]
            agency.last_pub = message.date
            agency.save()
            bot.send_message(chat_id, f'{p}', reply_markup=keyboard)
            agency = ProfileAgency.objects.get(agency_telegram_id=message.from_user.id)
            agency.last_pub = message.text
            bot.send_message(message.chat.id, 'Введите /start для продолжения работы', reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, 'Не могу найти такой проект', reply_markup=hideBoard)
        agency_menu(message)


def enter_project_id_for_edit(message):
    project = Project.objects.filter(pk=message.text)
    if project.exists():
        edit_project(message, project[0])
    else:
        bot.send_message(message.chat.id, 'Не могу найти такого проекта, введите /start, чтобы продолжить')


def agency_menu_choose(message, agency):
    hideBoard = types.ReplyKeyboardRemove()
    agency_menu_bar = telebot.types.ReplyKeyboardMarkup()
    agency_menu_bar.row('Опубликовать вакансию', 'Список активных вакансий 30 дней')
    agency_menu_bar.row('Изменить вакансию', 'Повторная публикация вакансии')
    agency_menu_bar.row('Изменить/добавить данные в анкете')
    agency_menu_bar.row('Оставить отзыв о промоутере', 'Оценить промоутера')
    request_list = telebot.types.ReplyKeyboardMarkup()
    request_list.row('Подтвержденные отклики', 'Неподтвержденные отклики')
    choice_for_edit = telebot.types.ReplyKeyboardMarkup()
    choice_for_edit.row('Добавить', 'Изменить')
    if message.text == 'Опубликовать вакансию':
        first_step_project_reg(message)
    elif message.text == 'Список активных вакансий 30 дней':
        agency = ProfileAgency.objects.get(agency_telegram_id=message.from_user.id)
        agency.get_projects(message)
    elif message.text == 'Изменить вакансию':
        bot.send_message(message.chat.id, 'Введите ID проекта для изменения', reply_markup=hideBoard)
        bot.register_next_step_handler(message, enter_project_id_for_edit)
    elif message.text == 'Повторная публикация вакансии':
        bot.send_message(message.chat.id, 'Введите ID проекта для повторной публикации', reply_markup=hideBoard)
        bot.register_next_step_handler(message, project_repeat, agency)
    elif message.text == 'Изменить/добавить данные в анкете':
        edit_agency(message)
    elif message.text == 'Оставить отзыв о промоутере':
        promo_review_reg(message)
    elif message.text == 'Оценить промоутера':
        promo_rate_reg(message)
    else:
        agency = ProfileAgency.objects.get(agency_telegram_id=message.from_user.id)
        bot.send_message(message.chat.id, f'{agency.real_name}, \n\n'
                                          f'Для начала работы, выберите пункт меню', reply_markup=agency_menu_bar)
        bot.register_next_step_handler(message, agency_menu_choose)


def agency_menu(message):
    hideBoard = types.ReplyKeyboardRemove()
    agency = ProfileAgency.objects.get(agency_telegram_id=message.from_user.id)
    agency_menu_bar = telebot.types.ReplyKeyboardMarkup()
    agency_menu_bar.row('Опубликовать вакансию', 'Список активных вакансий 30 дней')
    agency_menu_bar.row('Изменить вакансию', 'Повторная публикация вакансии')
    agency_menu_bar.row('Изменить/добавить данные в анкете')
    agency_menu_bar.row('Оставить отзыв о промоутере', 'Оценить промоутера')
    hello_message = day_time_no_city()
    bot.send_message(message.chat.id, f'{agency.real_name}, {hello_message}\n\n'
                                      f'Для начала работы, выберите пункт меню', reply_markup=agency_menu_bar)
    bot.register_next_step_handler(message, agency_menu_choose, agency)
