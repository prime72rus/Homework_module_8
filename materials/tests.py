from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """
    Тестировние CRUD модели Lesson
    """

    def setUp(self):
        """
        Подготовка данных для тестирования
        """
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
        """
        Тест просмотра урока
        """
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("title"), self.lesson.title)
        self.assertEqual(temp_data.get("owner"), self.lesson.owner.pk)

    def test_lesson_create(self):
        """
        Тест создания урока и проверки валидатора URL
        """
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
                    "Допускаются только "
                    "HTTPS-ссылки на конкретные видео YouTube"
                ]
            },
        )
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """
        Тест обновления урока
        """
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"title": "Test update"}
        response = self.client.patch(url, data)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("title"), "Test update")

    def test_lesson_delete(self):
        """
        Тест удаления урока
        """
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """
        Тест получения списка уроков
        """
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
                        "amount": 0
                    }
                ],
            },
        )


class SubscriptionTestCase(APITestCase):
    """
    Тест создания и удаления подписки
    """

    def setUp(self):
        """
        Подготовка данных для тестирования
        """
        self.user = User.objects.create(email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test", description="Test")

    def test_add_subscription(self):
        """
        Тест добавления подписки
        """
        url = reverse("materials:subscription")
        data = {
            "course": self.course.id,
            "user": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subscription(self):
        """
        Тест удаления подписки
        """
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("materials:subscription")
        data = {"course": self.course.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user, course=self.course
            ).exists()
        )

    def test_missing_course_id(self):
        """
        Тест отсутствия course_id в запросе
        """
        url = reverse("materials:subscription")
        data = {}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "course обязательное поле")

    def test_invalid_course_id(self):
        """
        Тест несуществующего course_id
        """
        url = reverse("materials:subscription")
        data = {"course": 999}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """
        Тест доступа неавторизованного пользователя
        """
        self.client.logout()

        url = reverse("materials:subscription")
        data = {"course_id": self.course.id}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
