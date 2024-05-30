from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserModeratorForm

from users.models import User
from .models import Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method')
    search_fields = ('user__username', 'course__title', 'lesson__title', 'payment_method')
    list_filter = ('payment_date', 'payment_method')
    ordering = ('-payment_date',)
