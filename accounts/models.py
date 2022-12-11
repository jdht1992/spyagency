import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager

BOSS = "1"
HITMEN = "2"

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    KIND_USER = [
        (BOSS, 'Boss'),
        (HITMEN, 'Hitmen'),
    ]
    kind = models.CharField(
        max_length=5,
        choices=KIND_USER,
        default=HITMEN,
    )
    username = None
    email = models.EmailField('email address', unique=True)
    lackeys = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_manager(self):
        return self.lackeys.all()

    def is_boss(self):
        return self.kind == BOSS

ASSIGNED = "1"
FAILED = "2"
COMPLETED = "3"


class Hit(models.Model):
    hitman = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hits", related_query_name='hit', on_delete=models.CASCADE)
    description = models.TextField()
    target_name = models.CharField(max_length=50)
    HIT_STATUS_CHOICES = [
        (ASSIGNED, 'Assigned'),
        (FAILED, 'Failed.'),
        (COMPLETED, 'Completed.'),
    ]
    status = models.CharField(
        max_length=5,
        choices=HIT_STATUS_CHOICES,
        default='OPEN',
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hits_author", related_query_name='hit_author', on_delete=models.CASCADE)

    def __str__(self):
        return self.target_name
