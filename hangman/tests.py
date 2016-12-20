from django.test import TestCase


class AnimalTestCase(TestCase):
    # TODO: Make a setup.
    def setUp(self):
        something = 1

    def test(self):
        self.assertEqual(1 + 1, 2)
