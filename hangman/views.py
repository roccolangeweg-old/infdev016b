from django.shortcuts import render, redirect, reverse
from .forms import GameCreateForm, GameMoveForm
from .models import Game, UserStatistics
from account.models import User
from django.http import Http404


def index(request):
    try:
        game = Game.objects.get(user=request.user, completed=False)
    except Game.DoesNotExist:
        return redirect(reverse('hangman:create'))

    return redirect(reverse('hangman:play', kwargs={'id': game.id}))


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
        game = Game.objects.get(pk=id, user=request.user, completed=False)
    except Game.DoesNotExist:
        return redirect(reverse('hangman:index'))

    if request.POST:
        form = GameMoveForm(request.POST, instance=game)
        if form.is_valid():
            form.save()

    form = GameMoveForm(instance=game)

    context = {
        'game': game,
        'form': form,
    }

    return render(request, template_name='hangman/play.html', context=context)


def score(request):
    users = User.objects.all()
    stats = []
    for u in users:
        user = [u.username, u.total_score()]
        stats.append(user)

    sorted_by_score = sorted(stats, key=lambda tup: tup[1], reverse=True)

    context = {
        'stats': sorted_by_score
    }

    return render(request, template_name='hangman/score.html', context=context)





