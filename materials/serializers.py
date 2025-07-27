from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import URLYouTubeValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [URLYouTubeValidator(field="link_video")]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source="lessons.all")
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        if hasattr(obj, "lessons_count"):
            return obj.lessons_count
        return 0

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=obj
            ).exists()
        return False

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "picture",
            "description",
            "lessons_count",
            "lessons",
            "owner",
            "amount",
            "is_subscribed",
        )
