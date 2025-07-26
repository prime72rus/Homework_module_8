from django.db.models import Count
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from users.permissions import IsModerator, IsNotModerator, IsOwner, IsSuperUser
from materials.paginators import MaterialPaginator


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")

        if not course_id:
            return Response(
                {"error": "course обязательное поле"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course
        )

        if not created:
            subscription.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MaterialPaginator

    def get_queryset(self):
        if self.action == "list" or self.action == "retrieve":
            return Course.objects.annotate(lessons_count=Count("lessons"))
        return Course.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, (IsNotModerator | IsSuperUser)]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [
                IsAuthenticated, (IsOwner | IsModerator | IsSuperUser)
            ]
        elif self.action == "destroy":
            self.permission_classes = [
                IsAuthenticated, (IsOwner | IsNotModerator | IsSuperUser)
            ]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner | IsSuperUser)]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotModerator]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner | IsSuperUser)]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsNotModerator, (IsOwner | IsSuperUser)]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
