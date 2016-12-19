from django import forms
from .models import Game, Word, Letter
import string


def get_alphabet_list():
    return list(string.ascii_lowercase)


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


class GameMoveForm(forms.ModelForm):

    letter = forms.ChoiceField(choices=get_alphabet_list())

    def __init__(self, *args, **kwargs):
        super(GameMoveForm, self).__init__(*args, **kwargs)
        letter_history = [ l.value for l in self.instance.letters.all() ]
        self.fields['letter'].choices = list([(l,l) for l in self.fields['letter'].choices if l not in letter_history])

    class Meta:
        model = Game
        fields = ('letter',)

    def save(self, commit=True):
        game = super(GameMoveForm, self).save(commit=False)

        letter = Letter.objects.get(value=self.cleaned_data['letter'])
        game.add_letter(letter)

        if commit:
            game.save()

        return game




