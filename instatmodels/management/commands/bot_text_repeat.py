import telebot
from django.conf import settings
from telebot import types

from ...dates_times import time_convert
from ...models import bot


def repeat_all_messages(message):
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите /start или /help для работы с ботом', reply_markup=hideBoard)
