from django.test import TestCase
from .models import User
from django.test import Client


class AccountTestCase(TestCase):
    def setUp(self):
        c = Client()
        response = c.post('/register/', {'username': 'test', 'email': 'test@test.test', 'password1': 'temp1234', 'password2': 'temp1234'})

    def test_if_user_exists(self):
        user = User.objects.get(username="test")
        self.assertIsInstance(user, User)

    def test_login(self):
        c = Client()
        response = c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        self.assertRedirects(response, '/')

    def test_wrong_login(self):
        c = Client()
        response = c.post('/login/', {'username': 'banaan', 'password': 'appel'})
        self.assertIs(response.status_code, 200)

    def test_logout(self):
        c = Client()
        response = c.post('/login/', {'username': 'test@test.test', 'password': 'temp1234'})
        response = c.post('/logout/')
        self.assertRedirects(response, '/login/')
