from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, не заходивших более месяца,
    исключая суперпользователей и модераторов
    """
    users = get_user_model()
    one_month_ago = timezone.now() - timedelta(days=30)

    users.objects.filter(last_login__lt=one_month_ago, is_active=True).exclude(
        models.Q(is_superuser=True) | models.Q(groups__name="Moderators")
    ).update(is_active=False)
