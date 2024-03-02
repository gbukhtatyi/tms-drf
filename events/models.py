from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from events.tasks import event_created


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    meeting_time = models.DateTimeField(default=datetime.now)
    users = models.ManyToManyField(get_user_model(), related_name="events", verbose_name="Участники")

    def save(self, **kwargs):
        is_creating = self.id is None
        super().save(**kwargs)
        if is_creating:
            event_created.apply_async(args=[self.id])

    class Meta:
        ordering = ['-meeting_time']
        indexes = [
            models.Index(fields=("meeting_time",), name="meeting_time_index")
        ]
