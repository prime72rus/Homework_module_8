from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

from users.models import Payment, User
from users.serializers import (
    PaymentSerializer,
    UserListSerializer,
    UserSerializer,
    UserPublicListSerializer,
)


class UserListAPIView(ListAPIView):
    serializer_class = UserPublicListSerializer
    queryset = User.objects.all()


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserListSerializer
        return UserPublicListSerializer


class UserCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        if user != self.request.user:
            raise PermissionDenied(
                "Вы можете редактировать только свой профиль")
        return user

    def perform_update(self, serializer):
        if "password" in serializer.validated_data:
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
        else:
            serializer.save()


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        if user != self.request.user:
            raise PermissionDenied("Вы можете удалить только свой профиль")
        return user


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)
