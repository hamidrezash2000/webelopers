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


class Meeting(models.model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    capacity = models.IntegerField(max_length=6, default=0)
    start = models.TimeField(auto_now_add=True)
    end = models.TimeField(auto_now_add=True)
    date = models.TimeField(auto_now_add=True)
