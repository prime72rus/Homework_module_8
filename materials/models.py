from django.db import models
from django.core.validators import URLValidator


class Course(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Курс"
    )
    picture = models.ImageField(
        upload_to="courses/pictures/",
        blank=True,
        null=True,
        verbose_name="Картинка"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Урок"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    picture = models.ImageField(
        upload_to="lessons/pictures",
        blank=True,
        null=True,
        verbose_name="Картинка"
    )
    link_video = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[URLValidator(schemes=["https"])],
        verbose_name="Ссылка на видео"
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lessons",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
