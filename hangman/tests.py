from django.test import TestCase
from account.models import User
from .models import Game
from .models import Difficulty
from .models import Word
from django.test import Client


class HangmanTestCase(TestCase):
    # TODO: Make a setup.
    def setUp(self):
        c = Client()
        c.post('/register/', {'username': 'test', 'email': 'test@test.test', 'password1': 'temp1234', 'password2': 'temp1234'})
        Difficulty.objects.create(label="normal", multiplier="2", amount_of_tries="10")
        Word.objects.create(word="testing")

    def test_create_game(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        self.assertIsInstance(difficulty, Difficulty)

        user = User.objects.get(username="test")
        response = c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user)
        self.assertIsInstance(game, Game)
        self.assertRedirects(response, '/hangman/play/'+str(game.id)+"/")



