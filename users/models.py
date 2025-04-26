from django.contrib.auth.models import AbstractUser
from core import models

class User(AbstractUser):
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
