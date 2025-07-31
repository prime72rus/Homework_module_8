from celery import shared_task
from celery.result import AsyncResult
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL
from materials.models import Course, Subscription


@shared_task(bind=True)
def send_email_about_update_course(self, course_id):
    """
    Отправка уведомления
    """
    course = Course.objects.get(pk=course_id)
    subscribers_emails = Subscription.objects.filter(
        course=course, user__email__isnull=False
    ).values_list("user__email", flat=True)
    if subscribers_emails:
        send_mail(
            subject=f"Обновление курса {course.title}",
            message=f"Курс {course.title}, на который вы подписаны, обновился",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=list(subscribers_emails),
        )


@shared_task(bind=True)
def schedule_course_notification(self, course_id):
    """
    Планирует уведомление через 4 часа с отменой
    предыдущих задач для этого курса
    """
    course = Course.objects.get(pk=course_id)
    if course.notification_task_id:
        AsyncResult(course.notification_task_id).revoke()

    task = send_email_about_update_course.apply_async(
        args=[course.id], countdown=2 * 60  # 4 часа в секундах
    )

    course.notification_task_id = task.id
    course.save()
