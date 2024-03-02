from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11, null=True, blank=True)
    is_subscribed = models.BooleanField(default=0)

    class Meta:
        db_table = "users"