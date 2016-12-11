from django.db import models
from django.conf import settings


class UserStatistics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    wins = models.IntegerField(default=0)
    forfeits = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)


class Words(models.Model):
    word = models.CharField(max_length=50)
