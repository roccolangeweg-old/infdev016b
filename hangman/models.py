from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid


# Statistics for a user in this game
class UserStatistics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    wins = models.IntegerField(default=0)
    forfeits = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)


# List of words to pick from
class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=50)

    def length(self):
        return len(self.word)

    def __str__(self):
        return self.word


# Difficulty reduces the amount of tries and increases the score multiplier.
class Difficulty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=50)
    multiplier = models.FloatField()
    amount_of_tries = models.IntegerField()

    def __str__(self):
        return '{} - {} tries ({}x multiplier)'.format(self.label, self.amount_of_tries, self.multiplier)


# Game is the current state of an active game
class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(Word)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    difficulty = models.ForeignKey(Difficulty)
    completed = models.BooleanField(default=False)
