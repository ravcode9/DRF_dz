from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Payment
from users.permissions import IsOwner, IsModer
from users.serializers import UserSerializer, PaymentSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['payment_date', 'amount']
    filterset_fields = ('lesson', 'course', 'payment_method', 'amount')


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModer]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModer]
