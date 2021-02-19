import telebot
from telebot import types
from django.contrib.auth import get_user_model
from django.db import models

from .data_check import project_status_check, true_check
from .dates_times import age_calculate, verified_status_text, time_convert, date_diff_project

# Основные модели проекта
TOKEN = '1349576678:AAGXnNV4k0We2CNwWvPnUmPW9PmpwEmCgNc'
bot = telebot.TeleBot(TOKEN)
chat_id = '-1001381518450'


class ProfilePromo(models.Model):
    promo_unique_id = models.TextField(
        verbose_name='ID пользователя',
        unique=True,
        null=True,
    )
    promo_telegram_id = models.PositiveIntegerField(null=True)
    promo_telegram_username = models.TextField()
    real_name = models.TextField(
        verbose_name='Реальное имя'
    )
    real_surname = models.TextField(null=True)
    real_secondName = models.TextField(null=True)
    phone_number = models.TextField(
        unique=True
    )
    birth_date = models.TextField(null=True)
    passport_data = models.IntegerField(
        unique=True,
        null=True
    )
    city = models.TextField(null=True)
    description = models.TextField()
    photo_1 = models.ImageField(null=True, blank=True, verbose_name='Фото анфас')  # Full-face photo
    photo_2 = models.ImageField(null=True, blank=True, verbose_name='Фото полный рост')  # Full-length photo
    photo_3 = models.ImageField(null=True, blank=True, verbose_name='Дополнительное фото 1')  # other photo
    photo_4 = models.ImageField(null=True, blank=True, verbose_name='Дополнительное фото 2')  # other photo
    photo_5 = models.ImageField(null=True, blank=True, verbose_name='Дополнительное фото 3')  # other photo
    verified_status = models.BooleanField(default=False)

    def __str__(self):
        return f'ФИО: {self.real_name} {self.real_surname} {self.real_surname}\n' \
               f'Возраст: {age_calculate(self.birth_date)}\n' \
               f'Номер телефона: {self.phone_number}\n' \
               f'Статус аккаунта: {verified_status_text(self.verified_status)}\n' \
               f'Город: {self.city}\n' \
               f'О себе: {self.description}'

    class Meta:
        verbose_name = 'Профиль промоутера'
        verbose_name_plural = 'Профили промоутеров'


class ProfileAgency(models.Model):
    agency_unique_id = models.TextField(
        verbose_name='ID агентства',
        unique=True,
        null=True
    )
    agency_telegram_id = models.TextField(null=True)
    agency_telegram_username = models.TextField(
        null=True
    )
    real_name = models.TextField(null=True)
    real_surname = models.TextField(null=True)
    phone_number = models.TextField(
        unique=True
    )
    agency_name = models.TextField(null=True)
    agency_phone_number = models.TextField(null=True)
    inn = models.IntegerField(
        unique=True,
        null=True
    )
    city = models.TextField(null=True)
    description = models.TextField()
    verified_status = models.BooleanField(default=False)
    agency_address = models.TextField(null=True, blank=True)
    agency_member_photo = models.ImageField(null=True, blank=True)
    promo_vacancy_picture = models.ImageField(null=True, blank=True)
    supervisor_vacancy_picture = models.ImageField(null=True, blank=True)
    helper_vacancy_picture = models.ImageField(null=True, blank=True)
    other_vacancy_picture = models.ImageField(null=True, blank=True)
    last_pub = models.TextField(null=True)

    def get_projects(self, message):
        p = self.projects.all()
        for i in p:
            diff = date_diff_project(i)
            if diff < 30:
                hideBoard = types.ReplyKeyboardRemove()
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text='Список откликов',
                                                             callback_data='all_promo')
                callback_button_2 = types.InlineKeyboardButton(text='Подтвержденных сотрудников',
                                                               callback_data='verified_promo')
                keyboard.add(callback_button)
                keyboard.add(callback_button_2)
                bot.send_message(message.chat.id, f'__________', reply_markup=hideBoard)
                bot.send_message(message.chat.id, f'{i}', reply_markup=keyboard, )

    def __str__(self):
        return f'ФИ: {self.real_name} {self.real_surname} \n' \
               f'Название агентства: {self.agency_name}\n' \
               f'Номер телефона: {self.phone_number}\n' \
               f'Номер телефона агентства: {self.agency_phone_number}\n' \
               f'Статус аккаунта: {verified_status_text(self.verified_status)}\n' \
               f'Город: {self.city}\n' \
               f'Информаци от агентства: {self.description}'

    class Meta:
        verbose_name = 'Профиль агентства'
        verbose_name_plural = 'Профили агентств'


class Rate(models.Model):
    rate = models.FloatField(null=True)
    pub_date = models.DateField(auto_now_add=True)


class RatePromo(Rate):
    promo = models.ForeignKey(ProfilePromo, on_delete=models.SET_NULL, related_name='rate', null=True)

    class Meta:
        verbose_name = 'Рейтинг промоутера'
        verbose_name_plural = 'Рейтинги промоутеров'


class RateAgency(Rate):
    agency = models.ForeignKey(ProfileAgency, on_delete=models.SET_NULL, related_name='rate', null=True)

    class Meta:
        verbose_name = 'Рейтинг агентства'
        verbose_name_plural = 'Рейтинги агентств'


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)


class ReviewPromo(Review):
    promo = models.ForeignKey(ProfilePromo, on_delete=models.SET_NULL, related_name='review', null=True)

    class Meta:
        verbose_name = 'Отзывы о промоутере'
        verbose_name_plural = 'Отзывы о промоутерах'

    def __str__(self):
        return f'Отзыв: {self.text}' \
               f'Сотрудник: {self.promo.promo_telegram_id}' \
               f'Отзыв опубликован {self.pub_date}'


class ReviewAgency(Review):
    agency = models.ForeignKey(ProfileAgency, on_delete=models.SET_NULL, related_name='review', null=True)

    class Meta:
        verbose_name = 'Отзыв об агентстве'
        verbose_name_plural = 'Отзывы об агентствах'

    def __str__(self):
        return f'Отзыв: {self.text}' \
               f'Агентство/Фриланс: {self.agency.agency_telegram_id}' \
               f'Отзыв опубликован: {self.pub_date}'


class Project(models.Model):
    project_name = models.TextField(unique=True)
    employers = models.TextField(null=True)
    project_employers = models.PositiveIntegerField(null=True)
    project_hours = models.PositiveIntegerField(null=True)
    project_addresses = models.TextField(null=True)
    costs_per_hour = models.PositiveIntegerField(null=True)
    form_for_employer = models.BooleanField(null=True)
    outside_project = models.BooleanField(null=True)
    every_day = models.BooleanField(null=True)
    start_date = models.TextField(null=True)
    end_date = models.TextField(null=True)
    project_description = models.TextField(null=True)
    city = models.TextField(null=True)
    pub_date = models.TextField(default='0')
    agency_project = models.ForeignKey(ProfileAgency, on_delete=models.SET_NULL, related_name='projects', null=True)

    def verified_promo_get(self, user, message):
        requests = self.promo_requests.all()
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text='Принять',
                                                     callback_data='accept_promo')
        callback_button_2 = types.InlineKeyboardButton(text='Отклонить',
                                                       callback_data='decline_promo')
        keyboard.add(callback_button, callback_button_2)
        for i in requests:
            if i.accept_status:
                bot.send_message(user.id, f'{i}', reply_markup=keyboard)

    def all_promo_get(self, user, message):
        requests = self.promo_requests.all()
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text='Принять',
                                                     callback_data='accept_promo')
        callback_button_2 = types.InlineKeyboardButton(text='Отклонить',
                                                       callback_data='decline_promo')
        keyboard.add(callback_button, callback_button_2)
        for i in requests:
            if not i.accept_status:
                bot.send_message(user.id, f'{i}', reply_markup=keyboard)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return f'ID агентства: {self.agency_project.agency_telegram_id}\n' \
               f'ID проекта: \n' \
               f'{self.pk}\n' \
               f'Ставка проекта: {self.costs_per_hour}\n' \
               f'Дата начала: {self.start_date}\n' \
               f'Дата окончания: {self.end_date}\n' \
               f'Статус проекта: {project_status_check(self.start_date, self.end_date)}\n' \
               f'Город: {self.city}\n' \
               f'Дата публикации: {time_convert(int(self.pub_date))}\n' \
               f'Текст вакансии для публикации:\n{self.project_description}'


class PromoRequest(models.Model):
    text = models.TextField(null=True)
    accept_status = models.BooleanField(default=False)
    pub_date = models.DateField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='promo_requests', null=True)
    promo = models.ForeignKey(ProfilePromo, on_delete=models.SET_NULL, related_name='promo_requests', null=True)

    class Meta:
        verbose_name = 'Запрос промоутера'
        verbose_name_plural = 'Запросы промоутеров'

    def __str__(self):
        return f'Oтклик на вакансию: {self.project.project_name},\n{self.pk}\nID проекта {self.project.pk}\n' \
               f'Агентство: {self.project.agency_project.agency_name}\n' \
               f'Отклик подтвержден на данный момент? - {true_check(self.accept_status)}\n' \
               f'Промоутер : \n' \
               f'{self.promo}'

# class Message(models.Model):
#     profile = models.ForeignKey(
#         to='instatmodels.Profile',
#         verbose_name='Профиль',
#         on_delete=models.PROTECT,
#     )
#     text = models.TextField(
#         verbose_name='Текст',
#     )
#     created_at = models.DateTimeField(
#         verbose_name='Время получения',
#         auto_now_add=True,
#     )
#
#     def __str__(self):
#         return f'Сообщение {self.pk} от {self.profile}'
#
#     class Meta:
#         verbose_name = 'Сообщение'
#         verbose_name_plural = 'Сообщения'
