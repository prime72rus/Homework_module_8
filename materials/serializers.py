from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source="lessons.all")

    def get_lessons_count(self, obj):
        if hasattr(obj, "lessons_count"):
            return obj.lessons_count
        return 0

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
        )
