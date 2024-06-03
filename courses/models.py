from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='название курса')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='превью', blank=True, null=True)
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', verbose_name='курс', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='название урока')
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='превью', blank=True, null=True)
    video_url = models.URLField(verbose_name='ссылка на видео', blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', blank=True, null=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, verbose_name='курс', blank=True, null=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.course}'
