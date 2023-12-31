from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import VoteUserManager


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class VoteUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ["email", "date_of_birth"]

    objects = VoteUserManager()


class Choice(models.Model):
    name = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    choices = models.ManyToManyField(Choice, related_name="related_polls", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Vote(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, related_name="votes", blank=True, null=True
    )
    choice = models.ForeignKey(
        Choice, on_delete=models.SET_NULL, related_name="votes", blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="votes",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.question.name} - {self.choice.name}"
