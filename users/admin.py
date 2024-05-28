from django.contrib import admin
from users.models import User
from .models import Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    ordering = ('date_joined',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method')
    search_fields = ('user__username', 'course__title', 'lesson__title', 'payment_method')
    list_filter = ('payment_date', 'payment_method')
    ordering = ('-payment_date',)
