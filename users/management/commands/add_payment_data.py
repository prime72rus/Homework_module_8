from django.core.management.base import BaseCommand
from materials.models import Course
from users.models import User, Payment


class Command(BaseCommand):
    help = "Создает тестовую запись о платеже пользователя"

    def handle(self, *args, **options):
        if User.objects.filter(email="first_user@example.com").exists():
            self.stdout.write(
                self.style.ERROR("Пользователь с таким email уже существует!")
            )
            return
        user = User.objects.create(
            email="first_user@example.com",
            phone="89999999999",
            city="Moscow",
            is_active=True,
        )
        user.set_password("Password2025")
        user.save()
        course = Course.objects.create(
            title="Профессия Python-разработчик",
            description="Python-разработчик — это программист, который "
                        "создаёт и поддерживает программное обеспечение с "
                        "использованием языка программирования Python.",
        )

        Payment.objects.create(
            user=user,
            paid_course=course,
            amount=20000,
        )
