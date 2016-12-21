from django.test import TestCase
from account.models import User
from .models import Game
from .models import Difficulty
from .models import Word
from .models import Letter
from django.test import Client


class HangmanTestCase(TestCase):
    # TODO: Make a setup.
    def setUp(self):
        c = Client()
        c.post('/register/', {'username': 'test', 'email': 'test@test.test', 'password1': 'temp1234', 'password2': 'temp1234'})
        Difficulty.objects.create(label="normal", multiplier="2", amount_of_tries="2")
        Word.objects.create(word="testing")
        Letter.objects.create(value="t", points="1")
        Letter.objects.create(value="e", points="1")
        Letter.objects.create(value="s", points="1")
        Letter.objects.create(value="i", points="1")
        Letter.objects.create(value="n", points="1")
        Letter.objects.create(value="g", points="1")
        Letter.objects.create(value="a", points="1")
        Letter.objects.create(value="b", points="1")

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

    def test_create_game_again(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        self.assertIsInstance(difficulty, Difficulty)

        user = User.objects.get(username="test")
        response = c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user)
        self.assertIsInstance(game, Game)
        self.assertRedirects(response, '/hangman/play/' + str(game.id) + "/")

        response = c.post('/hangman/create/')
        self.assertIs(response.status_code, 200)



    def test_do_correct_game_move(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user)
        lettervalue = "e"
        c.post('/hangman/play/'+str(game.id)+"/", {'letter': lettervalue})
        game = Game.objects.get(user=user)
        letter = Letter.objects.get(value=lettervalue)
        self.assertIs(game.score, int(letter.points*game.difficulty.multiplier))

    def test_do_incorrect_game_move(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user)
        lettervalue = "a"
        c.post('/hangman/play/'+str(game.id)+"/", {'letter': lettervalue})
        game = Game.objects.get(user=user)
        self.assertIs(game.failed_tries, 1)

    def test_win_game(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user)
        lettervalue = "t"
        c.post('/hangman/play/'+str(game.id)+"/", {'letter': lettervalue})
        lettervalue = "e"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': lettervalue})
        lettervalue = "s"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': lettervalue})
        lettervalue = "i"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': lettervalue})
        lettervalue = "n"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': lettervalue})
        lettervalue = "g"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': lettervalue})
        game = Game.objects.get(user=user)
        self.assertTrue(game.completed)

    def test_lose_game(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user)
        lettervalue = "a"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': lettervalue})
        lettervalue = "b"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': lettervalue})
        game = Game.objects.get(user=user)
        self.assertTrue(game.completed)
