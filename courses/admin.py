from django.contrib import admin

from courses.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'description',)
    list_filter = ('title',)
    search_fields = ('title', 'preview', 'description',)


@admin.register(Lesson)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'description', 'preview')
    list_filter = ('title',)
    search_fields = ('title', 'preview', 'description', 'course')
