from datetime import timedelta
from celery import shared_task
from users.models import User
from django.core.mail import send_mail
from django.utils import timezone
from courses.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)
        subscriber_emails = [subscription.user.email for subscription in subscriptions]
        if subscriber_emails:
            send_mail(
                'Уведомление об обновлении курса',
                f'Курс "{course.title}" был обновлен.',
                'manu_alex_ilov@mail.ru',
                subscriber_emails,
                fail_silently=False,
            )
    except Course.DoesNotExist:
        pass


@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
