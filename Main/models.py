from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Person(models.Model):
    GENDER_CHOICES = (
        ("M", "مرد"),
        ("F", "زن")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default="M")
    picture = models.FileField(upload_to="static/pictures/", null=True, blank=True)