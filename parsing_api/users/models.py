from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    units = models.IntegerField(default = 1000, blank = True)

    class Meta:
        verbose_name_plural = 'user'

    def __str__(self):
        return self.email
