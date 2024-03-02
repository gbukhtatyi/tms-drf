from datetime import datetime, timedelta
from celery import shared_task
from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.html import strip_tags


def get_event_model():
    return django_apps.get_model(app_label='events', model_name='Event')


@shared_task
def send_notification():
    notify_before_hour(5)
    notify_before_hour(23)


@shared_task
def notify_before_hour(hours):
    Event = get_event_model()

    datetime_start = datetime.now() + timedelta(hours=hours, minutes=15)
    datetime_end = datetime.now() + timedelta(hours=hours + 1)

    events = Event.objects.filter(
        meeting_time__gte=datetime_start,
        meeting_time__lte=datetime_end,
    )

    for event in events:
        html_message = f"<p>Date: {event.meeting_time}</p> {event.description}"
        plain_message = strip_tags(html_message)

        for user in event.users.all():
            send_mail(
                f"[Events App] Star event: {hours + 1}",
                plain_message,
                "info@events.local",
                [user.email],
                fail_silently=False,
                html_message=html_message
            )


@shared_task
def event_created(event_id):
    User = get_user_model()
    Event = get_event_model()

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        print("Event doesn't exists")

    users = User.objects.filter(is_subscribed=True)

    html_message = f"<p>Date: {event.meeting_time}</p> {event.description}"
    plain_message = strip_tags(html_message)

    for user in users:
        send_mail(
            f"[Events App] New event available: {event.name}",
            plain_message,
            "info@events.local",
            [user.email],
            fail_silently=False,
            html_message=html_message
        )
