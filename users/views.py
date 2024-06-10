from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User, Payment
from users.permissions import IsOwner, IsModer
from users.serializers import UserSerializer, PaymentSerializer, UserCreateSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session


class UserRegisterView(generics.CreateAPIView):
    """
    APIView для регистрации нового пользователя.

    Атрибуты:
        queryset: QuerySet для всех объектов пользователя.
        permission_classes: Разрешения для доступа к этому представлению.
        serializer_class: Класс сериализатора для объекта пользователя.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        """
        Создает нового пользователя и генерирует токены JWT.

        Аргументы:
            serializer: Сериализатор с данными пользователя.

        Возвращает:
            Response: Ответ с токенами доступа и обновления.
        """
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.

    Атрибуты:
        serializer_class: Класс сериализатора для объекта пользователя.
        queryset: QuerySet для всех объектов пользователя.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """
    APIView для получения списка платежей.

    Атрибуты:
        serializer_class: Класс сериализатора для объекта платежа.
        queryset: QuerySet для всех объектов платежа.
        filter_backends: Бэкенды для фильтрации и сортировки платежей.
        ordering_fields: Поля, по которым можно сортировать платежи.
        filterset_fields: Поля, по которым можно фильтровать платежи.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['payment_date', 'amount']
    filterset_fields = ('lesson', 'course', 'payment_method', 'amount')


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """
    APIView для получения одного платежа.

    Атрибуты:
        queryset: QuerySet для всех объектов платежа.
        serializer_class: Класс сериализатора для объекта платежа.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """
    APIView для обновления платежа.

    Атрибуты:
        queryset: QuerySet для всех объектов платежа.
        serializer_class: Класс сериализатора для объекта платежа.
        permission_classes: Разрешения для доступа к этому представлению.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModer]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """
    APIView для удаления платежа.

    Атрибуты:
        queryset: QuerySet для всех объектов платежа.
        serializer_class: Класс сериализатора для объекта платежа.
        permission_classes: Разрешения для доступа к этому представлению.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModer]


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    APIView для создания нового платежа.

    Атрибуты:
        queryset: QuerySet для всех объектов платежа.
        serializer_class: Класс сериализатора для объекта платежа.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Сохраняет новый платеж с текущим пользователем в качестве владельца.

        Аргументы:
            serializer: Сериализатор с данными платежа.
        """
        payment = serializer.save(user=self.request.user)
        course = payment.course
        lesson = payment.lesson

        if course:
            product_name = course.title
        elif lesson:
            product_name = lesson.title
        else:
            raise ValueError("Payment must be associated with either a course or a lesson.")

        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(product_id, payment.amount)

        success_url = "http://127.0.0.1:8000/courses/"
        cancel_url = "http://127.0.0.1:8000/courses/"

        session_id, checkout_url = create_stripe_checkout_session(price_id, success_url, cancel_url)

        payment.stripe_product_id = product_id
        payment.stripe_price_id = price_id
        payment.stripe_session_id = session_id
        payment.stripe_checkout_url = checkout_url
        payment.save()

        return Response({
            'payment': PaymentSerializer(payment).data,
            'checkout_url': checkout_url
        })
