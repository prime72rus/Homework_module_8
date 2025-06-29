from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import PaymentViewSet
from users.views import UserCreateAPIView, UserListAPIView, UserDetailAPIView, UserDeleteAPIView, UserUpdateAPIView

app_name = UsersConfig.name

router = DefaultRouter()
# router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentViewSet, basename="payments")
urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
    path("users/register/", UserCreateAPIView.as_view(), name="user_register"),
    path("users/delete/<int:pk>/", UserDeleteAPIView.as_view(), name="user_delete"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),


    path(
        "users/login/", TokenObtainPairView.as_view(), name="login"
    ),
    path(
        "users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
] + router.urls
