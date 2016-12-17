from django import forms
from .models import Game, Word


class GameCreateForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('difficulty',)

    def save(self, user, commit=True):
        game = super(GameCreateForm, self).save(commit=False)
        game.word = Word.objects.order_by('?').first()
        game.user = user

        if Game.objects.filter(user=user, completed=False):
            raise forms.ValidationError("User already has an active game")

        if commit:
            game.save()

        return game


