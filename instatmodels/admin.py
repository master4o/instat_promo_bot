from django.contrib import admin

# from .forms import ProfileForm
from .models import (ProfileAgency, ProfilePromo, Project, PromoRequest,
                     RateAgency, RatePromo, ReviewAgency, ReviewPromo)


@admin.register(ProfileAgency)
class ProfileAgencyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'agency_unique_id', 'agency_telegram_id', 'agency_telegram_username',
                    'real_name', 'real_surname', 'phone_number', 'agency_name', 'inn', 'city', 'verified_status',)
    search_fields = ('real_name', 'real_surname', 'promo_unique_id', 'city', 'verified_status',)
    empty_value_display = '-пусто-'
    # form = ProfileForm


@admin.register(ProfilePromo)
class ProfilePromoAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'promo_unique_id', 'promo_telegram_id', 'promo_telegram_username', 'real_name', 'real_surname',
        'phone_number', 'city', 'verified_status',)
    search_fields = ('real_name', 'real_surname', 'agency_unique_id', 'city', 'verified_status',)
    empty_value_display = '-пусто-'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'project_name', 'project_hours', 'start_date', 'end_date', 'get_agency_unique_id',)
    search_fields = ('current_status_active', 'start_date', 'end_date', 'agency_project',)
    empty_value_display = '-пусто-'

    def get_agency_unique_id(self, obj):
        return obj.agency_project.agency_unique_id

    get_agency_unique_id.short_description = 'agency_unique_id'
    get_agency_unique_id.admin_order_field = 'agency_project'


@admin.register(ReviewPromo)
class ReviewPromoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'get_promo_unique_id',)
    search_fields = 'get_promo_unique_id',
    empty_value_display = '-пусто-'

    def get_promo_unique_id(self, obj):
        return obj.promo.promo_unique_id

    get_promo_unique_id.short_description = 'promo_unique_id'
    get_promo_unique_id.admin_order_field = 'review_promo'


@admin.register(RatePromo)
class RatePromoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'get_promo_unique_id',)
    search_fields = 'get_promo_unique_id',
    empty_value_display = '-пусто-'

    def get_promo_unique_id(self, obj):
        return obj.promo.promo_unique_id

    get_promo_unique_id.short_description = 'promo_unique_id'
    get_promo_unique_id.admin_order_field = 'rate_promo'


@admin.register(ReviewAgency)
class ReviewAgencyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'get_agency_unique_id')
    search_fields = 'get_agency_unique_id',
    empty_value_display = '-пусто-'

    def get_agency_unique_id(self, obj):
        return obj.agency.agency_unique_id

    get_agency_unique_id.short_description = 'agency_unique_id'
    get_agency_unique_id.admin_order_field = 'review_agency'


@admin.register(RateAgency)
class RateAgencyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'get_agency_unique_id',)
    search_fields = 'get_agency_unique_id',
    empty_value_display = '-пусто-'

    def get_agency_unique_id(self, obj):
        return obj.agency.agency_unique_id

    get_agency_unique_id.short_description = 'agency_unique_id'
    get_agency_unique_id.admin_order_field = 'rate_agency'


@admin.register(PromoRequest)
class PromoRequestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_project_unique_id', 'get_promo_unique_id', 'accept_status',)
    search_fields = ('pk', 'get_project_unique_id', 'get_promo_unique_id', 'accept_status',)
    empty_value_display = '-пусто-'

    def get_project_unique_id(self, obj):
        return obj.project.pk

    get_project_unique_id.short_description = 'project_unique_id'
    get_project_unique_id.admin_order_field = 'request_project'

    def get_promo_unique_id(self, obj):
        return obj.promo.promo_unique_id

    get_promo_unique_id.short_description = 'promo_unique_id'
    get_promo_unique_id.admin_order_field = 'request_promo'



#
#
# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'profile', 'text', 'created_at')
