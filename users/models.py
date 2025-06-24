from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=65,
        verbose_name="Город",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cach", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey("User", on_delete=models.SET_NULL, blank=True, null=True, related_name="users", verbose_name="Пользователь")
    payment_date = models.DateTimeField()
    paid_course = models.ForeignKey("materials.Course", on_delete=models.SET_NULL, blank=True, null=True, related_name="users", verbose_name="Оплаченный курс")
    paid_lesson = models.ForeignKey("materials.Lesson", on_delete=models.SET_NULL, blank=True, null=True, related_name="users", verbose_name="Оплаченный урок")
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="cach", verbose_name="Способ оплаты")

    def __str__(self):
        return f"{self.user} - {self.payment_date} - {self.amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
