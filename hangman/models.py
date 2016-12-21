from django.db import models
from django.conf import settings
from django.contrib import messages
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


# Letters in the alphabet supported as answers
class Letter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.CharField(max_length=1)
    points = models.IntegerField(default=100)


# Game is the current state of an active game
class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(Word)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    difficulty = models.ForeignKey(Difficulty)
    completed = models.BooleanField(default=False)
    failed_tries = models.IntegerField(default=0)
    letters = models.ManyToManyField(Letter)
    score = models.IntegerField(default=0)

    def tries_left(self):
        return self.difficulty.amount_of_tries - self.failed_tries

    def add_failed_try(self):
        self.failed_tries += 1
        if not self.tries_left():
            self.completed = True

    def get_letters(self):
        return [l.value for l in self.letters.all()]

    def add_letter(self, letter):
        self.letters.add(letter)

        if letter.value in self.word.word:
            self.score += letter.points * self.difficulty.multiplier
            if self.solved():
                pass
        else:
            self.add_failed_try()

    def solved(self):
        self.completed = not len([l for l in self.word.word if l not in self.get_letters()]) > 1
        return self.completed

    def has_won(self):
        return self.completed and self.failed_tries < self.difficulty.amount_of_tries

