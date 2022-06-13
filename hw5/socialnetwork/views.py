from django.shortcuts import render, redirect, get_object_or_404
from socialnetwork.forms import LoginForm, ProfileForm, RegisterForm
from django.urls import reverse
from django.http import Http404, HttpResponse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from socialnetwork.models import *

# Create your views here.

@login_required
def profile_page(request):
    if (request.method == 'GET'):
        context = {'profile' : request.user.profile,
                    'form' : ProfileForm(initial={'bio' : request.user.profile.bio})}
        return render(request, 'socialnetwork/profile.html', context)
    
    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'profile': request.user.profile, 'form': form}
        return render(request, 'socialnetwork/profile.html', context)
    
    pic = form.cleaned_data['picture']
    request.user.profile.picture = pic
    request.user.profile.bio = form.cleaned_data['bio']
    if form.cleaned_data['picture']:
        request.user.profile.content_type = form.cleaned_data['picture'].content_type
    request.user.profile.save()
    context = {
        'profile': request.user.profile,
        'form' : form
    }
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def get_photo(request, id):
    profilepic = get_object_or_404(Profile, id=id)

    if not profilepic.picture:
        raise Http404
    
    return HttpResponse(profilepic.picture, content_type=profilepic.content_type)

@login_required
def follow(request, id):
    if (request.method == 'POST'):
        user_follow = get_object_or_404(User, id=id)
        request.user.profile.following.add(user_follow)
        request.user.profile.save()
        return render(request, 'socialnetwork/other.html', {'profile': user_follow.profile})

@login_required
def unfollow(request, id):
    if (request.method == 'POST'):
        user_unfollow = get_object_or_404(User, id=id)
        request.user.profile.following.remove(user_unfollow)
        request.user.profile.save()
    return render(request, 'socialnetwork/other.html', {'profile': user_unfollow.profile})

@login_required
def other_profile(request, id):
    if (request.method == 'GET'):
        user = get_object_or_404(User, id=id)
        context = {}
        context['profile'] = user.profile
        return render(request, 'socialnetwork/other.html', context)

@login_required
def follower_page(request):
    if (request.method == 'GET'):
        context = {}
        context['posts'] = Post.objects.all().order_by('-time')
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
    
    new_profile = Profile(user=new_user)
    new_profile.save()

    login(request, new_user)
    return redirect(reverse('home'))

@login_required
def global_page(request):
    if (request.method == 'GET'):
        return render(request, 'socialnetwork/global.html', { 'posts': Post.objects.all().order_by('-time') })

    if 'text' not in request.POST or not request.POST['text']:
        context = { 'message': 'invalid text' }
        return render(request, 'socialnetwork/global.html', context)

    new_post = Post(text=request.POST['text'], user=request.user, time=timezone.now())
    new_post.save()
    return render(request, 'socialnetwork/global.html', { 'posts': Post.objects.all().order_by('-time') })
