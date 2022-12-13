from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    class Kind(models.TextChoices):
        BOSS = 'boss', _('Boss')
        HITMEN = 'hitmen', _('Hitmen')

    kind = models.CharField(
        max_length=10,
        choices=Kind.choices,
        default=Kind.HITMEN,
    )
    description = models.TextField()
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
        return self.kind == self.Kind.BOSS


class Hit(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', _('Open')
        ASSIGNED = 'assigned', _('Assigned')
        FAILED = 'failed', _('Failed')
        COMPLETED = 'completed', _('Completed')

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
    )
    hitman = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hits", related_query_name='hit', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    target_name = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hits_author", related_query_name='hit_author', on_delete=models.CASCADE)

    def __str__(self):
        return self.target_name
