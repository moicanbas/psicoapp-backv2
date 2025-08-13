from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    identification = models.CharField(max_length=50, null=True)
    birthdate = models.DateField(null=True)

    def __str__(self):
        return self.username
