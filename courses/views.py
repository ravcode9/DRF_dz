from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsOwner, IsModer
from .models import Course, Lesson, Subscription
from .paginators import CourseLessonPaginator
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.

    Атрибуты:
        queryset: QuerySet для всех объектов курса.
        serializer_class: Класс сериализатора для объекта курса.
        pagination_class: Класс пагинатора для курса и его уроков.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPaginator

    def perform_create(self, serializer):
        """
        Сохраняет новый курс с текущим пользователем в качестве владельца.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Возвращает QuerySet в зависимости от роли пользователя.
        Если пользователь суперпользователь или модератор, возвращает все курсы.
        Иначе возвращает только курсы текущего пользователя.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        """
        Возвращает список разрешений в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner, ~IsModer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """
    APIView для создания урока.

    Атрибуты:
        queryset: QuerySet для всех объектов урока.
        serializer_class: Класс сериализатора для объекта урока.
        permission_classes: Разрешения для доступа к этому представлению.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """
        Сохраняет новый урок с текущим пользователем в качестве владельца.
        """
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    APIView для получения списка уроков.

    Атрибуты:
        serializer_class: Класс сериализатора для объекта урока.
        queryset: QuerySet для всех объектов урока.
        permission_classes: Разрешения для доступа к этому представлению.
        pagination_class: Класс пагинатора для уроков.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPaginator


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    APIView для обновления урока.

    Атрибуты:
        serializer_class: Класс сериализатора для объекта урока.
        queryset: QuerySet для всех объектов урока.
        permission_classes: Разрешения для доступа к этому представлению.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    APIView для удаления урока.

    Атрибуты:
        queryset: QuerySet для всех объектов урока.
        serializer_class: Класс сериализатора для объекта урока.
        permission_classes: Разрешения для доступа к этому представлению.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    APIView для получения одного урока.

    Атрибуты:
        serializer_class: Класс сериализатора для объекта урока.
        queryset: QuerySet для всех объектов урока.
        permission_classes: Разрешения для доступа к этому представлению.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
    APIView для создания подписки на курс.

    Атрибуты:
        queryset: QuerySet для всех объектов подписки.
        serializer_class: Класс сериализатора для объекта подписки.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Создает или удаляет подписку на курс для текущего пользователя.

        Аргументы:
            request: Запрос, содержащий данные о курсе.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            Response: Ответ с сообщением о результате операции.
        """
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_201_CREATED)
