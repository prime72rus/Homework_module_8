from django.db.models import Count
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.action == "list" or self.action == "retrieve":
            return Course.objects.annotate(lessons_count=Count("lessons"))
        return Course.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [
                IsAuthenticated & (IsOwner | IsModerator)
            ]
        elif self.action == "destroy":
            self.permission_classes = [
                IsAuthenticated & (IsOwner | ~IsModerator)
            ]
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated & ~IsModerator]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated & IsOwner & ~IsModerator]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
