from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.utils.translation import ugettext as _

from .forms import RegistrationForm


def login(request):
    login_form = AuthenticationForm()

    if request.user.is_authenticated():
        return redirect('/')
    if request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('/')

    context = {
        'form': login_form,
    }
    return render(request, template_name='account/login.html', context=context)


def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.WARNING, _('You\'ve been logged out.'))
    return redirect(reverse('login'))


def register(request):
    register_form = RegistrationForm()

    if request.user.is_authenticated():
        return redirect('/')
    if request.POST:
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, _('Your account has been registered.'))
            return redirect('/')

    context = {
        'form': register_form
    }

    return render(request, template_name='account/register.html', context=context)