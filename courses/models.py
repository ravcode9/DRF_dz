from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='название курса')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='превью', blank=True, null=True)
    description = models.TextField(verbose_name='описание', blank=True, null=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', verbose_name='курс', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='название урока')
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='превью', blank=True, null=True)
    video_url = models.URLField(verbose_name='ссылка на видео', blank=True, null=True)

    def __str__(self):
        return self.title
