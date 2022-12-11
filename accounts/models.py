import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    KIND_USER = [
        ('1', 'Boss'),
        ('2', 'Hitmen'),
    ]
    kind = models.CharField(
        max_length=5,
        choices=KIND_USER,
        default='Boss',
    )
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
