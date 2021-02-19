import telebot
from telebot import types

from ...models import (ProfileAgency, ProfilePromo, Project, PromoRequest,
                       RateAgency, RatePromo, ReviewAgency, ReviewPromo, bot)

hideBoard = types.ReplyKeyboardRemove()


def enter_request_text(message, p):
    project = p
    agency = project.agency_project
    promo = ProfilePromo.objects.get(promo_telegram_id=message.from_user.id)
    text = message.text
    agency_telegram_id = agency.agency_telegram_id
    r = PromoRequest(
        project=project,
        promo=promo,
        text=text
    )
    r.save()
    bot.send_message(message.chat.id, 'Ваш отклик зарегистрирован, работодателю отправлены все нобходимые данные.'
                                      'После того, как работодатель подтвердит вашу кандидатуру, я сразу же дам вам '
                                      'знать')
    bot.send_message(agency_telegram_id, f'На вашу вакансию {project.project_name}\n'
                                         f'Откликнулся сотрудник {promo.real_name}\n'
                                         f'ID сотрудника {promo.promo_telegram_id}\n'
                                         f'Текст отлика: {text}')


def request_reg(message):
    if Project.objects.filter(project_name=message.text)[0].exists():
        bot.send_message(message.chat.id, 'Введите текст для отправки отклика работодателю', reply_markup=hideBoard)
        p = Project.objects.get(pk=message.text)
        bot.register_next_step_handler(message, enter_request_text, p)
    else:
        bot.send_message(message.chat.id, 'Не могу найти такого проекта, что-то пошло не так', reply_markup=hideBoard)


def request_reg_from(from_user, message):
    p = ProfilePromo.objects.filter(promo_telegram_id=from_user.id).exists()
    if p:
        project_id = message.text.splitlines()
        project_id = project_id[2]
        p = Project.objects.get(pk=project_id)
        bot.send_message(from_user.id, 'Введите текст отклика')
        bot.register_next_step_handler_by_chat_id(from_user.id, enter_request_text, p)
    else:
        bot.send_message(from_user.id, 'Вы не сотрудник :)')
        bot.send_sticker(from_user.id, 'CAACAgQAAxkBAAK6uWAKxiv5ElWDh9dZVRlcaNZd49K0AAI_AQACqCEhBigP01yXNi1sHgQ')
