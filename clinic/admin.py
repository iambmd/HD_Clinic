from django.contrib import admin

from .models import Appointment, Article, ContactMessage, Doctor, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_vi', 'category', 'icon']
    list_filter = ['category']
    search_fields = ['title_en', 'title_vi']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty']
    search_fields = ['name', 'specialty']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'published_date', 'slug']
    list_filter = ['published_date']
    search_fields = ['title_en', 'title_vi']
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published_date'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'preferred_date', 'preferred_time', 'branch', 'created_at']
    list_filter = ['branch', 'preferred_date']
    search_fields = ['full_name', 'phone', 'email']
    readonly_fields = ['created_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'sent_at']
    search_fields = ['name', 'phone', 'email', 'message']
    readonly_fields = ['sent_at']
