from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name="Токен", blank=True, null=True)
    is_active = models.BooleanField(default='True', verbose_name='активность')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"
        ordering = ['email']


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', verbose_name='пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
