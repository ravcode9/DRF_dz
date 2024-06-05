from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson, Subscription

User = get_user_model()


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.ru', password='123')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='test course', owner=self.user)
        self.lesson = Lesson.objects.create(title='test lesson', course=self.course,
                                            video_url='https://www.youtube.com/123', owner=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            'title': 'New Lesson',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/abc'
        }
        response = self.client.post('/lesson/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Lesson')

    def test_read_lesson(self):
        """Тестирование чтения урока"""
        response = self.client.get(f'/lesson/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test lesson')

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        data = {
            'title': 'Updated Lesson'
        }
        response = self.client.patch(f'/lesson/update/{self.lesson.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Lesson')

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        response = self.client.delete(f'/lesson/delete/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.ru', password='123')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="test", owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_create_subscription(self):
        """Тестирование создания подписки"""
        data = {
            "course_id": self.course.id,
        }

        response = self.client.post(reverse('courses:subscription-create'), data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'message': 'Подписка удалена'}
        )