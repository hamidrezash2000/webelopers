from django.contrib.auth.models import User
from django.db import models
import datetime

class Person(models.Model):
    GENDER_CHOICES = (
        ("M", "مرد"),
        ("F", "زن")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default="M")
    picture = models.FileField(upload_to="static/pictures/", null=True, blank=True)


class Meeting(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    start = models.TimeField()
    end = models.TimeField()
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Teacher Free Times"

