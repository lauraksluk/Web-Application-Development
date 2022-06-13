from django.shortcuts import render, redirect
from socialnetwork.forms import LoginForm, RegisterForm
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def profile_page(request):
    if (request.method == 'GET'):
        context = {}
        return render(request, 'socialnetwork/profile.html', context)

@login_required
def follower_page(request):
    if (request.method == 'GET'):
        context = {}
        return render(request, 'socialnetwork/follower.html', context)

def login_context():
    context = {}
    context['form'] = LoginForm()
    return context

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def login_page(request):
    if (request.method == 'GET'):
        context = login_context()
        return render(request, 'socialnetwork/login.html', context)

    context = {}
    form = LoginForm(request.POST)
    context['form'] = form

    if (not form.is_valid()):
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def register_page(request):
    if(request.method == 'GET'):
        context = {}
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)
    
    context = {}
    form = RegisterForm(request.POST)
    context['form'] = form

    if (not form.is_valid()):
        return render(request, 'socialnetwork/register.html', context)
    
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

@login_required
def global_page(request):
    if (request.method == 'GET'):
        context = {}
        return render(request, 'socialnetwork/global.html', context)

@login_required
def other_profile(request):
    if (request.method == 'GET'):
        context = {"follow": True,}
        return render(request, 'socialnetwork/other.html', context)


