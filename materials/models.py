from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Курс")
    picture = models.ImageField(
        upload_to="courses/pictures/",
        blank=True,
        null=True,
        verbose_name="Картинка",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Урок")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )
    picture = models.ImageField(
        upload_to="lessons/pictures",
        blank=True,
        null=True,
        verbose_name="Картинка",
    )
    link_video = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lessons",
        verbose_name="Курс",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="courses",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на курс: {self.course}"
