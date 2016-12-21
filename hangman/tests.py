from django.test import TestCase
from account.models import User
from .models import Game
from .models import Difficulty
from .models import Word
from .models import Letter
from .models import UserStatistics
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
        game = Game.objects.get(user=user, completed=False)
        self.assertIsInstance(game, Game)
        self.assertRedirects(response, '/hangman/play/'+str(game.id)+"/")

    def test_create_game_again(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        self.assertIsInstance(difficulty, Difficulty)

        user = User.objects.get(username="test")
        response = c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user, completed=False)
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
        game = Game.objects.get(user=user, completed=False)
        letter_value = "e"
        c.post('/hangman/play/'+str(game.id)+"/", {'letter': letter_value})
        game = Game.objects.get(user=user, completed=False)
        letter = Letter.objects.get(value=letter_value)
        self.assertIs(game.score, int(letter.points*game.difficulty.multiplier))

    def test_do_incorrect_game_move(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user, completed=False)
        letter_value = "a"
        c.post('/hangman/play/'+str(game.id)+"/", {'letter': letter_value})
        game = Game.objects.get(user=user, completed=False)
        self.assertIs(game.failed_tries, 1)

    def test_win_game(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user, completed=False)
        letter_value = "t"
        c.post('/hangman/play/'+str(game.id)+"/", {'letter': letter_value})
        letter_value = "e"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "s"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "i"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "n"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "g"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        game = Game.objects.filter(user=user, completed=True).order_by('-id')[0]
        self.assertTrue(game.completed)
        self.assertIs(user.total_score(), game.score)

    def test_win_two_games(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user, completed=False)
        letter_value = "t"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "e"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "s"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "i"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "n"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "g"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        game = Game.objects.get(user=user)
        self.assertTrue(game.completed)
        self.assertIs(user.total_score(), game.score)
        old_score = game.score

        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user, completed=False)
        letter_value = "t"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "e"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "s"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "i"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "n"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "g"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        game = Game.objects.filter(user=user, completed=True).order_by('-id')[0]
        self.assertTrue(game.completed)
        self.assertIs(user.total_score(), game.score + old_score)

    def test_lose_game(self):
        c = Client()
        c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        difficulty = Difficulty.objects.get(label="normal")
        user = User.objects.get(username="test")
        c.post('/hangman/create/', {'difficulty': difficulty.id})
        game = Game.objects.get(user=user, completed=False)
        letter_value = "a"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        letter_value = "b"
        c.post('/hangman/play/' + str(game.id) + "/", {'letter': letter_value})
        game = Game.objects.filter(user=user, completed=True).order_by('-id')[0]
        self.assertTrue(game.completed)
