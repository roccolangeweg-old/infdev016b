from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    wins = models.IntegerField(default=0)
    forfeits = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)


class Words(models.Model):
    word = models.CharField(max_length=50)
