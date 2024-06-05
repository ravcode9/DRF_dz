from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[YouTubeLinkValidator])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_amount(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='user.email', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course']
