from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import (
    PaymentSerializer,
    UserListSerializer,
    UserPublicListSerializer,
    UserSerializer,
)
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
    get_stripe_payment_status,
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
                "Вы можете редактировать только свой профиль"
            )
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

    def perform_create(self, serializer):
        payment_data = serializer.validated_data
        user = self.request.user

        if payment_data.get("paid_course"):
            paid_item = payment_data["paid_course"]
            item_type = "Курс"
        elif payment_data.get("paid_lesson"):
            paid_item = payment_data["paid_lesson"]
            item_type = "Урок"
        else:
            raise ValidationError("Не указан курс или урок для оплаты")

        amount = paid_item.amount

        product_name = f"{item_type}: {paid_item.title}"
        product = create_stripe_product(product_name)
        stripe_price = create_stripe_price(amount, product)

        session_id, payment_url, payment_status = create_stripe_session(
            stripe_price.id
        )

        serializer.save(
            amount=amount,
            session_id=session_id,
            payment_link=payment_url,
            payment_status=payment_status,
            user=user,
            payment_method="transfer",
        )


class PaymentUpdateAPIView(UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        session_id = instance.session_id
        payment_status = get_stripe_payment_status(session_id)
        instance.payment_status = payment_status
        instance.save()

        return super().partial_update(request, *args, **kwargs)
