from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

from tests.app.constants import IDLE, STATUS_CHOICES


class Stuff(models.Model):
    """Simple stuff model with status."""

    status = models.CharField(default=IDLE, max_length=32, choices=STATUS_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]
