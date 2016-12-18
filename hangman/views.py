from django.shortcuts import render, redirect, reverse
from .forms import GameCreateForm
from .models import Game, UserStatistics
from django.http import Http404


def index(request):
    try:
        game = Game.objects.get(user=request.user)
    except Game.DoesNotExist:
        return redirect(reverse('hangman:create'))

    return redirect(reverse('hangman:play', kwargs={'id': game.id }))


def create(request):
    form = GameCreateForm()

    if request.POST:
        form = GameCreateForm(request.POST)
        if form.is_valid():
            game = form.save(user=request.user)
            return redirect(reverse('hangman:play', kwargs={'id': game.id}))

    context = {
        'form': form
    }

    return render(request, template_name='hangman/create.html', context=context)


def play(request, id):
    try:
        game = Game.objects.get(pk=id, user=request.user)
    except Game.DoesNotExist:
        return Http404()

    tries = str(game.difficulty.amount_of_tries)

    hangman = ""

    guesslist = ["a", "b", "c", "d"]

    for letter in game.word.word.lower():
        if letter in guesslist:
            hangman += letter + ' '
        else:
            hangman += '_ '

    context = {
        'game': game,
        'hangman': hangman,
        'tries': tries
    }

    return render(request, template_name='hangman/play.html', context=context)


def score(request):
    stats = UserStatistics.objects.all().order_by('-wins')

    context = {
        'stats': stats
    }

    return render(request, template_name='hangman/score.html', context=context)





