from django.db.models import Count
from rest_framework.generics import (
    CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerators


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.action == "list" or self.action == "retrieve":
            return Course.objects.annotate(lessons_count=Count("lessons"))
        return Course.objects.all()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModerators,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerators,)
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsModerators)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, ~IsModerators)
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsModerators)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, ~IsModerators)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
