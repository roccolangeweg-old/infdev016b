from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from hangman.models import Game
import uuid


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def total_score(self):
        return sum([g.score for g in self.game_set.all() if g.has_won()])

    def hangman_wins(self):
        return [g for g in self.game_set.all() if g.has_won()]

    def hangman_losses(self):
        return [g for g in self.game_set.all() if g.has_lost()]
