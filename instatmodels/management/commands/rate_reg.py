import telebot
from telebot import types

from ...models import ProfileAgency, ProfilePromo, RateAgency, RatePromo, bot


def promo_enter_rate(message, promo):
    hideBoard = types.ReplyKeyboardRemove()
    if 0 <= float(message.text) <= 5:
        promo_rate = RatePromo(
            rate=float(message.text),
            promo=ProfilePromo.objects.get(promo_unique_id=promo)
        )
        promo_rate.save()
        bot.send_message(message.chat.id, 'Ваша оценка учтена, благодарим за обратную связь, это помогает в '
                                          'будущем выбирать лучший персонал для ваших проектов', reply_markup=hideBoard)
    else:
        enter_promo_id(message)


def enter_promo_id(message):
    promo_select_reg = telebot.types.ReplyKeyboardMarkup()
    promo_select_reg.row('1', '2', '3', '4', '5')
    if ProfilePromo.objects.filter(promo_unique_id=message.text).exists():
        promo = message.text
        bot.send_message(message.chat.id, 'Выберите оценку', reply_markup=promo_select_reg)
        bot.register_next_step_handler(message, promo_rate_reg, promo)
    else:
        bot.send_message(message.chat.id, 'Не могу найти такого промоутера')
        promo_rate_reg(message)


def promo_rate_reg(message):
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите ID промоутера для регистрации вашей оценки', reply_markup=hideBoard)
    bot.register_next_step_handler(message, promo_enter_rate)


def agency_enter_rate(message, agency):
    hideBoard = types.ReplyKeyboardRemove()
    if 0 <= float(message.text) <= 5:
        agency_rate = RateAgency(
            rate=float(message.text),
            agency=ProfileAgency.objects.get(agency_unique_id=agency)
        )
        agency_rate.save()
        bot.send_message(message.chat.id, 'Ваша оценка учтена, благодарим за обратную связь, это помогает '
                                          'работать с лучшими агентствами', reply_markup=hideBoard)
    else:
        enter_agency_id(message)


def enter_agency_id(message):
    agency_select_reg = telebot.types.ReplyKeyboardMarkup()
    agency_select_reg.row('1', '2', '3', '4', '5')
    if ProfileAgency.objects.filter(agency_unique_id=message.text).exists():
        agency = message.text
        bot.send_message(message.chat.id, 'Выберите оценку', reply_markup=agency_select_reg)
        bot.register_next_step_handler(message, promo_rate_reg, agency)
    else:
        bot.send_message(message.chat.id, 'Не могу найти такое агентство')
        agency_rate_reg(message)


def agency_rate_reg(message):
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите ID агентства для регистрации вашей оценки', reply_markup=hideBoard)
    bot.register_next_step_handler(message, enter_agency_id)
