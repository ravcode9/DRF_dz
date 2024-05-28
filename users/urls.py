from django.urls import path, include

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView, \
    PaymentUpdateAPIView, PaymentDestroyAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-detail'),
    path('payment/<int:pk>/update/', PaymentUpdateAPIView.as_view(), name='payment-update'),
    path('payment/<int:pk>/delete/', PaymentDestroyAPIView.as_view(), name='payment-delete'),
] + router.urls
