from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from materials.models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test", description="Test")
        self.lesson = Lesson.objects.create(
            title="Test",
            description="Test",
            course=self.course,
            owner=self.user,
        )

    def test_lesson_detail(self):
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("title"), self.lesson.title)
        self.assertEqual(temp_data.get("owner"), self.lesson.owner.pk)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test",
            "description": "Test",
            "course": self.course.pk,
            "link_video": "https://www.youtube.com/watch?v=NjsQuBZ--w0",
        }
        data_invalid_url = {
            "title": "Test",
            "description": "Test",
            "link_video": "http://www.youtube.com/watch?v=NjsQuBZ--w0",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        response = self.client.post(url, data_invalid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        temp_data = response.json()
        self.assertEqual(
            temp_data,
            {
                "non_field_errors": [
                    "Допускаются только HTTPS-ссылки на конкретные видео YouTube"
                ]
            },
        )
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"title": "Test update"}
        response = self.client.patch(url, data)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("title"), "Test update")

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        temp_data = response.json()

        self.assertEqual(
            temp_data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "picture": None,
                        "link_video": None,
                        "course": self.lesson.course.pk,
                        "owner": self.lesson.owner.pk,
                    }
                ],
            },
        )
