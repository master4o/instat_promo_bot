import telebot
from telebot import types

from ...models import (ProfileAgency, ProfilePromo, RateAgency, RatePromo,
                       ReviewAgency, ReviewPromo, bot)

hideBoard = types.ReplyKeyboardRemove()


def promo_enter_review(message, promo):
    promo_rate = ReviewPromo(
        promo=ProfilePromo.objects.get(promo_unique_id=promo),
        text=message.text
    )
    promo_rate.save()
    bot.send_message(message.chat.id, 'Ваша отзыв записан, благодарим за обратную связь, это помогает в '
                                      'будущем выбирать лучший персонал для ваших проектов', reply_markup=hideBoard)


def enter_promo_id(message):
    if ProfilePromo.objects.filter(promo_unique_id=message.text).exists():
        promo = message.text
        bot.send_message(message.chat.id, 'Введите отзыв о работе с промоутером')
        bot.register_next_step_handler(message, promo_enter_review, promo)
    else:
        bot.send_message(message.chat.id, 'Не могу найти такого промоутера')
        promo_review_reg(message)


def promo_review_reg(message):
    bot.send_message(message.chat.id, 'Введите ID промоутера для регистрации вашего отзыва', reply_markup=hideBoard)
    bot.register_next_step_handler(message, enter_promo_id)


def agency_enter_review(message, agency):
    agency_review = ReviewAgency(
        text=message.text,
        agency=ProfileAgency.objects.get(agency_unique_id=agency)
    )
    agency_review.save()
    bot.send_message(message.chat.id, 'Ваш отзыв учтен, благодарим за обратную связь, это помогает '
                                      'работать с лучшими агентствами', reply_markup=hideBoard)


def enter_agency_id(message):
    if ProfileAgency.objects.filter(agency_unique_id=message.text).exists():
        agency = message.text
        bot.send_message(message.chat.id, 'Выберите оценку')
        bot.register_next_step_handler(message, agency_enter_review, agency)
    else:
        bot.send_message(message.chat.id, 'Не могу найти такое агентство')
        agency_review_reg(message)


def agency_review_reg(message):
    bot.send_message(message.chat.id, 'Введите ID агентства для регистрации вашего отзыва', reply_markup=hideBoard)
    bot.register_next_step_handler(message, enter_agency_id)
