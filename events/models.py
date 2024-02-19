from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    meeting_time = models.DateTimeField(default=datetime.now)
    users = models.ManyToManyField(get_user_model(), related_name="events", verbose_name="Участники")

    class Meta:
        ordering = ['-meeting_time']
        indexes = [
            models.Index(fields=("meeting_time",), name="meeting_time_index")
        ]