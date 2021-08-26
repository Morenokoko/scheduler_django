from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
import datetime as dt


class Availability(models.Model):
    user = models.ForeignKey(User, null=True,  on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    shift = models.TimeField(default=dt.time(00, 00), auto_now=False, auto_now_add=False)
    # shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(default=0, blank=False, validators=[MinValueValidator(1), MaxValueValidator(24)])
    class Meta:
        unique_together = (("user", "date", "shift"), ("user", "date", "rank"))
    def __str__(self):
        availability_id = '{0.date} {0.user} {0.shift}'
        return availability_id.format(self)


class Schedule(models.Model):
    date = models.DateField()
    shift = models.TimeField(default=dt.time(00, 00), auto_now=False, auto_now_add=False)
    # shift = models.ForeignKey(Shift, null=True, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ("date", "shift")
    def __str__(self):
        schedule_id = '{0.date} {0.shift}'
        return schedule_id.format(self)