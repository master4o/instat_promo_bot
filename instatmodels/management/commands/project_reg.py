import telebot
from telebot import types

from ...data_check import birth_date_check, project_status_check, true_check, digit_check
from ...dates_times import what_time_django, time_convert
import datetime as dt
from ...models import ProfileAgency, ProfilePromo, Project, bot, chat_id


def project_last_step_reg(message, project_name, project_employers, project_hours, project_form, project_outside,
                          project_cost, project_start_date, project_end_date, project_city):
    project_end_reg = telebot.types.ReplyKeyboardMarkup()
    project_end_reg.row('-Опубликовать-', '-Start-')
    project_name = project_name
    project_employers = project_employers
    project_hours = project_hours
    project_form = project_form
    project_outside = project_outside
    project_cost = project_cost
    project_start_date = project_start_date
    project_end_date = project_end_date
    project_city = project_city
    project_description = message.text
    bot.send_message(message.chat.id, f'Проект готов к публикации, давайте еще раз все проверим\n\n'
                                      f'Название проекта: {project_name}\n'
                                      f'Количество персонала, необходимое в проекте: {project_employers}\n'
                                      f'Количество часов на сотрудника: {str(project_hours)}\n'
                                      f'Есть ли форма одежды от заказчика: {true_check(project_form)}\n'
                                      f'Проект на улице? -{true_check(project_outside)}\n'
                                      f'Стоиомсть часа работы на проекте: {project_cost}\n'
                                      f'Дата начала проекта: {project_start_date}\n'
                                      f'Дата окончания проекта: {project_end_date}\n'
                                      f'Текущий статус проекта: '
                                      f'{project_status_check(project_start_date, project_end_date)}\n'
                                      f'Город: {project_city}\n'
                                      f'Текст вакансии: \n'
                                      f'{project_description}')
    bot.send_message(message.chat.id, 'Если все данные указаны верно - нажмите -Опубликовать-\n'
                                      'Если хотите зарегистрировать вакансию еще раз - нажмите -Start-',
                     reply_markup=project_end_reg)
    bot.register_next_step_handler(message, end_project_reg, project_name, project_employers, project_hours,
                                   project_form, project_outside, project_cost, project_start_date, project_end_date,
                                   project_city, project_description)


def enter_project_city(message, project_name, project_employers, project_hours, project_form, project_outside,
                       project_cost, project_start_date, project_end_date):
    project_city = message.text.capitalize()
    bot.send_message(message.chat.id, 'Введите произвольный текст вакансии. Рекомендуем описать вакансию как можно '
                                      'подробнее')
    bot.register_next_step_handler(message, project_last_step_reg, project_name, project_employers, project_hours,
                                   project_form, project_outside, project_cost, project_start_date, project_end_date,
                                   project_city)


def enter_project_end_date(message, project_name, project_employers, project_hours, project_form, project_outside,
                           project_cost, project_start_date):
    check = birth_date_check(message.text)
    if check == 1:
        project_end_date = message.text
        bot.send_message(message.chat.id, 'Введите город, в котором будет проходить проект (на каждый город, в '
                                          'данной версии бота, необходима новая вакансия, мы работаем над '
                                          'расширением функционала')
        bot.register_next_step_handler(message, enter_project_city, project_name, project_employers,
                                       project_hours, project_form, project_outside, project_cost,
                                       project_start_date, project_end_date)
    elif check == 2:
        bot.send_message(message.chat.id, 'Вы ввели дату в неверном формате, введите дату старта проекта в формате '
                                          'дд.мм.гггг')
        bot.register_next_step_handler(message, enter_project_end_date, project_name, project_employers,
                                       project_hours, project_form, project_outside, project_cost, project_start_date)
    else:
        bot.send_message(message.chat.id, 'Не удалось проверить правильность ввода даты в формате дд.мм.гггг, '
                                          'введите дату ещё раз')
        bot.register_next_step_handler(message, enter_project_end_date, project_name, project_employers,
                                       project_hours, project_form, project_outside, project_cost, project_start_date)


def enter_project_start_date(message, project_name, project_employers, project_hours, project_form, project_outside,
                             project_cost):
    check = birth_date_check(message.text)
    if check == 1:
        project_start_date = message.text
        bot.send_message(message.chat.id, 'Введите дату окончания проекта в формате дд.мм.гггг')
        bot.register_next_step_handler(message, enter_project_end_date, project_name, project_employers,
                                       project_hours, project_form, project_outside, project_cost,
                                       project_start_date)
    elif check == 2:
        bot.send_message(message.chat.id, 'Вы ввели дату в неверном формате, введите дату старта проекта в формате '
                                          'дд.мм.гггг')
        bot.register_next_step_handler(message, enter_project_start_date, project_name, project_employers,
                                       project_hours, project_form, project_outside, project_cost)
    else:
        bot.send_message(message.chat.id, 'Не удалось проверить правильность ввода даты в формате дд.мм.гггг, '
                                          'введите дату ещё раз')
        bot.register_next_step_handler(message, enter_project_start_date, project_name, project_employers,
                                       project_hours, project_form, project_outside, project_cost)


def enter_project_cost(message, project_name, project_employers, project_hours, project_form, project_outside):
    if digit_check(message.text):
        project_cost = int(message.text)
        bot.send_message(message.chat.id, 'Введите дату начала проекта в формате дд.мм.гггг')
        bot.register_next_step_handler(message, enter_project_start_date, project_name, project_employers,
                                       project_hours, project_form, project_outside, project_cost)
    else:
        bot.send_message(message.chat.id, 'Введите стоимость часа цифрами, без лишних знаков и букв')
        bot.register_next_step_handler(message, enter_project_cost, project_name, project_employers, project_hours,
                                       project_form, project_outside)


def enter_project_outside(message, project_name, project_employers, project_hours, project_form):
    outside_choice = telebot.types.ReplyKeyboardMarkup()
    outside_choice.row('На улице', 'В помещении')
    if message.text == 'На улице':
        project_outside = True
        bot.send_message(message.chat.id, 'Оплата за час (укажите оплату в рублях основной позиции, оплату остальных'
                                          'позиций ваксансию можно уточнить в описании вакансии через 2 шага)')
        bot.register_next_step_handler(message, enter_project_cost, project_name, project_employers, project_hours,
                                       project_form, project_outside)
    elif message.text == 'В помещении':
        project_outside = False
        bot.send_message(message.chat.id, 'Оплата за час (укажите оплату в рублях основной позиции, оплату остальных'
                                          'позиций ваксансию можно уточнить в описании вакансии через 2 шага)')
        bot.register_next_step_handler(message, enter_project_cost, project_name, project_employers, project_hours,
                                       project_form, project_outside)
    else:
        bot.send_message(message.chat.id, 'Необходимо ли персоналу использовать форму от клиента?',
                         reply_markup=outside_choice)
        bot.register_next_step_handler(message, enter_project_outside, project_name, project_employers,
                                       project_hours, project_form)


def enter_project_form(message, project_name, project_employers, project_hours):
    project_outside = telebot.types.ReplyKeyboardMarkup()
    project_outside.row('На улице', 'В помещении')
    form_choice = telebot.types.ReplyKeyboardMarkup()
    form_choice.row('Да', 'Нет')
    if message.text == 'Да':
        project_form = True
        bot.send_message(message.chat.id, 'Проект на улице?', reply_markup=project_outside)
        bot.register_next_step_handler(message, enter_project_outside, project_name, project_employers, project_hours,
                                       project_form)
    elif message.text == 'Нет':
        project_form = False
        bot.send_message(message.chat.id, 'Проект на улице?', reply_markup=project_outside)
        bot.register_next_step_handler(message, enter_project_outside, project_name, project_employers, project_hours,
                                       project_form)
    else:
        bot.send_message(message.chat.id, 'Необходимо ли персоналу использовать форму от клиента?',
                         reply_markup=form_choice)
        bot.register_next_step_handler(message.text, enter_project_form, project_name, project_employers, project_hours)


def enter_project_hours(message, project_name, project_employers):
    form_choice = telebot.types.ReplyKeyboardMarkup()
    form_choice.row('Да', 'Нет')
    if digit_check(message.text) == 1:
        project_hours = int(message.text)
        bot.send_message(message.chat.id, 'Необходимо ли персоналу использовать форму от клиента?',
                         reply_markup=form_choice)
        bot.register_next_step_handler(message, enter_project_form, project_name, project_employers, project_hours)
    else:
        bot.send_message(message.chat.id, 'Введите часы цифрой')
        bot.register_next_step_handler(message, enter_project_hours, project_name, project_employers)


def enter_project_employers(message, project_name):
    project_employers = message.text
    bot.send_message(message.chat.id, 'Введите общее количество часов на одного сотрудника(если количество часов на '
                                      'разных сотрудников отличается - введите максимальное количество часов на '
                                      'сотрудника')
    bot.register_next_step_handler(message, enter_project_hours, project_name, project_employers)


def enter_project_name(message):
    project_name = message.text
    bot.send_message(message.chat.id, 'Введите количество персонала, необходимое для проекта')
    bot.register_next_step_handler(message, enter_project_employers, project_name)


def first_step_project_reg(message):
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите название проекта', reply_markup=hideBoard)
    bot.register_next_step_handler(message, enter_project_name)


def end_project_reg(message, project_name, project_employers, project_hours,
                    project_form, project_outside, project_cost, project_start_date, project_end_date,
                    project_city, project_description):
    if message.text == '-Опубликовать-':
        proj = Project(
            project_name=project_name,
            project_employers=project_employers,
            project_hours=project_hours,
            form_for_employer=project_form,
            outside_project=project_outside,
            costs_per_hour=project_cost,
            start_date=project_start_date,
            end_date=project_end_date,
            city=project_city,
            project_description=project_description,
            agency_project=ProfileAgency.objects.filter(agency_telegram_id=message.from_user.id)[0],
            pub_date=message.date
        )
        proj.save()
        agency = ProfileAgency.objects.get(agency_telegram_id=message.from_user.id)
        now_time = what_time_django()
        pub_time = time_convert(int(agency.last_pub))
        now_time = dt.datetime.strptime(now_time, '%d.%m.%Y - %H:%M:%S')
        pub_time = dt.datetime.strptime(pub_time, '%d.%m.%Y - %H:%M:%S')
        diff = now_time - pub_time
        if diff < 3600:
            bot.send_message(message.chat.id, f'Опубликовать вакансию можно только раз в час. До повторной '
                                              f'публикации осталось {60 - (round((diff.seconds / 60), 0))} мин '
                                              f'{60 - (diff.seconds % 60)} сек\n'
                                              f'Опубликуйте вакансию позже через главное меню с помощью '
                                              f'функции "Повторная публикация".')

        else:
            bot.send_message(chat_id, f'{proj}')
            bot.send_message(message.chat.id, 'Вакансия создана и опубликована\n '
                                              'Вы сможете повторно опубликовать созданную вакансию из главного меню '
                                              'позже. Обращаем ваше внимание на то, что вакансия одна и та же вакансия '
                                              'от одного и того же агентсва публикуется не чаще, чем один раз в час.')
            bot.send_message(message.chat.id, 'Введите команду /start для продолжения работы с ботом.')
            agency.last_pub = message.date

    else:
        first_step_project_reg(message)
