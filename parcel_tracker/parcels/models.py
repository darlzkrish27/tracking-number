# Create your models here.
# parcels/models.py
from django.db import models
from django.utils import timezone
import uuid

class TrackingNumber(models.Model):
    tracking_number = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(default=timezone.now)