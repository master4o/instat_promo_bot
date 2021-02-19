from ...models import ProfileAgency, ProfilePromo, Project, bot
import telebot
from telebot import types
from ...data_check import birth_date_check, digit_check


def edit_description(message, project):
    description = message.text
    project.project_description = description
    bot.send_message(message.chat.id, f'Теперь описание проекта:\n{description}\n')
    edit_project(message, project)


def edit_end_date(message, project):
    end_date = message.text
    check = birth_date_check(end_date)
    if check == 1:
        project.end_date = end_date
        project.save()
        bot.send_message(message.chat.id, f'Теперт дата окончания проекта - {project.start_date}\n')
        edit_project(message, project)
    elif check == 0:
        bot.send_message(message.chat.id, 'Дату старта необходимо ввести в формате дд.мм.гггг')
        edit_project(message, project)


def edit_start_date(message, project):
    start_date = message.text
    check = birth_date_check(start_date)
    if check == 1:
        project.start_date = start_date
        project.save()
        bot.send_message(message.chat.id, f'Теперт дата старта проект - {project.start_date}\n')
        edit_project(message, project)
    elif check == 0:
        bot.send_message(message.chat.id, 'Дату старта необходимо ввести в формате дд.мм.гггг')
        edit_project(message, project)


def edit_cost(message, project):
    check = digit_check(message.text)
    if check == 1:
        project.costs_per_hour = message.text
        project.save()
        bot.send_message(message.chat.id, f'Теперь стоимость часа - {project.costs_per_hour}\n')
        edit_project(message, project)
    elif check == 0:
        bot.send_message(message.chat.id, 'Стомость необходимо ввести числом')
        edit_project(message, project)


def edit_hours(message, project):
    check = digit_check(message.text)
    if check == 1:
        project.project_hours = message.text
        project.save()
        bot.send_message(message.chat.id, f'Теперь количество часов на проекте - {project.project_hours}\n')
        edit_project(message, project)
    elif check == 0:
        bot.send_message(message.chat.id, 'Количество часов необходимо ввести числом')
        edit_project(message, project)


def edit_employers(message, project):
    check = digit_check(message.text)
    if check == 1:
        project.project_employers = message.text
        project.save()
        bot.send_message(message.chat.id, f'Теперь на проект требуется человек - {project.project_employers}\n')
        edit_project(message, project)
    elif check == 0:
        bot.send_message(message.chat.id, 'Количество работников необходимо ввести числом')
        edit_project(message, project)


def edit_project_choose(message, project):
    hideBoard = types.ReplyKeyboardRemove()
    if message.text == 'Количество людей':
        employers = project.project_employers
        bot.send_message(message.chat.id, f'Сейчас на проект требуется количество людей - {employers}\n'
                                          f'Введите новое значение')
        bot.register_next_step_handler(message, edit_employers, project)
    elif message.text == 'Количество часов':
        hours = project.project_hours
        bot.send_message(message.chat.id, f'Сейчас количество часов на человека - {hours}\n'
                                          f'Введите новое значение')
        bot.register_next_step_handler(message, edit_hours, project)
    elif message.text == 'Стоимость часа':
        cost = project.costs_per_hour
        bot.send_message(message.chat.id, f'Сейчас на проекте оплата в час - {cost}\n'
                                          f'Введите новое значение')
        bot.register_next_step_handler(message, edit_cost, project)
    elif message.text == 'Дата начала проекта':
        start_date = project.start_date
        bot.send_message(message.chat.id, f'Сейчас дата старта проекта - {start_date}\n'
                                          f'Введите новое значение в формате дд.мм.гггг')
        bot.register_next_step_handler(message, edit_start_date, project)
    elif message.text == 'Дата окончания проекта':
        end_date = project.end_date
        bot.send_message(message.chat.id, f'Сейчас дата окончания проекта - {end_date}\n'
                                          f'Введите новое значение в формате дд.мм.гггг')
        bot.register_next_step_handler(message, edit_end_date, project)
    elif message.text == 'Описание проекта':
        description = project.project_description
        bot.send_message(message.chat.id, f'Сейчас описание проекта:\n{description}\n'
                                          f'Введите новое описание')
        bot.register_next_step_handler(message, edit_description, project)
    else:
        bot.send_message(message.chat.id, 'Введите /start, чтобы продолжить', reply_markup=hideBoard)


def edit_project(message, project):
    project_edit_bar = telebot.types.ReplyKeyboardMarkup()
    project_edit_bar.row('Количество людей', 'Количество часов')
    project_edit_bar.row('Стоимость часа', 'Дата начала проекта')
    project_edit_bar.row('Дата окончания проекта', 'Описание проекта')
    bot.send_message(message.chat.id, 'Выберите, что хотите изменить в вакансии', reply_markup=project_edit_bar)
    bot.register_next_step_handler(message, edit_project_choose, project)
