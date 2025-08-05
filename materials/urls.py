from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView,
    LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView,
    SubscriptionAPIView
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lesson_detail",
    ),
    path(
        "lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"
    ),
    path(
        "lessons/update/<int:pk>/",
        LessonUpdateAPIView.as_view(),
        name="lesson_update",
    ),
    path(
        "lessons/delete/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lesson_delete",
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
] + router.urls
