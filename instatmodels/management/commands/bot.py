import re

import telebot
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from telebot import types

from ...data_check import (birth_date_check, correct_entry, phone_check,
                           word_lang_check)
from ...dates_times import (age_calculate, day_time_city, day_time_no_city,
                            time_convert, what_time, what_time_general)
from ...encodeID import encode_id
from ...models import (ProfileAgency, ProfilePromo, Project, PromoRequest,
                       RateAgency, RatePromo, ReviewAgency, ReviewPromo, bot,
                       chat_id)
from .agency_menu import agency_menu
from .agency_reg import agency_first_step_reg
from .bot_text_repeat import repeat_all_messages
from .project_reg import first_step_project_reg
from .promo_menu import promo_menu
from .promo_reg import promo_first_step_reg
from .request_reg import request_reg_from


def recover_acc(message):
    p = ProfilePromo.objects.filter(promo_telegram_id=message.text).exists()
    a = ProfileAgency.objects.filter(agency_telegram_id=message.text).exists()
    if p:
        bot.send_message(message, 'Ваш профиль сотрудника восстановлен')
        p = ProfilePromo.objects.filter(promo_telegram_id=message.text)[0]
        p.promo_telegram_id = message.from_user.id
        p.save()
    elif a:
        bot.send_message(message, 'Ваш профиль работодателя восстановлен')
        a = ProfileAgency.objects.filter(agency_telegram_id=message.text)[0]
        a.agency_telegram_id = message.from_user.id
        a.save()
    else:
        bot.send_message(message, 'Такой аккаунт не найден')


def choose_role(message):
    hideBoard = types.ReplyKeyboardRemove()
    if message.text == 'Хочу работать':
        promo_first_step_reg(message)
    elif message.text == 'Я представляю агентство/фриланс':
        agency_first_step_reg(message)
    else:
        bot.send_message(message.chat.id, 'Придётся начать заново, введите /reg', reply_markup=hideBoard)


def reg_process(message):
    role_keyboard = telebot.types.ReplyKeyboardMarkup()
    role_keyboard.row('Хочу работать', 'Я представляю агентство/фриланс')
    if message.text == 'Завершить регистрацию':
        new_commands = telebot.types.ReplyKeyboardMarkup()
        new_commands.row('Публикация вакансии', 'Покажи активные проекты')
        bot.send_message(message.chat.id, 'Вы только что закончили регистрацию, новые команды к вашим услугам',
                         reply_markup=new_commands)
    else:
        bot.send_message(message.chat.id, 'Выберите вашу роль', reply_markup=role_keyboard)
        bot.register_next_step_handler(message, choose_role)


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        hideBoard = types.ReplyKeyboardRemove()

        @bot.message_handler(func=lambda msg: msg.text == 'выход')
        def end(message):
            bot.send_message(message.chat.id, 'Добро пожаловать в главное меню')
            start(message)

        @bot.message_handler(commands=['recover'])
        def recover(message):
            bot.send_message(message.chat.id, 'Введите старый telegram_id для восстановления доступа к аккаунту',
                             reply_markup=hideBoard)
            bot.register_next_step_handler(message, recover_acc)

        @bot.message_handler(commands=['start'])
        def start(message):
            p = ProfilePromo.objects.filter(promo_telegram_id=message.from_user.id).exists()
            a = ProfileAgency.objects.filter(agency_telegram_id=message.from_user.id).exists()
            if p:  # Если найдено совпадение в бд Сотрудников
                promo_menu(message)
            elif a:  # Если найдено совпадение в бд Агентств
                agency_menu(message)
            else:
                hello_message = day_time_no_city()
                bot.send_message(message.chat.id, f'{message.from_user.first_name}, {hello_message}\n\n'
                                                  f'Для начала работы, необходимо пройти быструю процедуру'
                                                  f' регистрации, она займет не больше минуты.', reply_markup=hideBoard)
                reg_process(message)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.data == 'request':
                request_reg_from(call.from_user, call.message)
            elif call.data == 'verified_promo':
                project_id = call.message.text.splitlines()
                project_id = project_id[2]
                p = Project.objects.get(pk=project_id)
                p.verified_promo_get(call.from_user, call.message)
            elif call.data == 'all_promo':
                project_id = call.message.text.splitlines()
                project_id = project_id[2]
                p = Project.objects.get(pk=project_id)
                p.all_promo_get(call.from_user, call.message)
            elif call.data == 'accept_promo':
                request_id = call.message.text.splitlines()
                request_id = request_id[1]
                r = PromoRequest.objects.get(pk=request_id)
                r.accept_status = True
                r.save()
            elif call.data == 'decline_promo':
                request_id = call.message.text.splitlines()
                request_id = request_id[1]
                r = PromoRequest.objects.get(pk=request_id)
                r.accept_status = False
                r.save()

        @bot.message_handler(content_types=['text'])
        def text_command(message):
            repeat_all_messages(message)

        @bot.message_handler(commands=['help'])
        def help_command(message):
            bot.send_message(message.chat.id, 'Если у вас есть предложения/жалобы/благодарности, просьба адресовать '
                                              'их напрямую в службу поддержки - @instatmng')

        bot.infinity_polling()
