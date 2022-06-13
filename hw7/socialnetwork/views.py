from django.shortcuts import render, redirect, get_object_or_404
from socialnetwork.forms import LoginForm, ProfileForm, RegisterForm
from django.urls import reverse
from django.http import Http404, HttpResponse 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone, dateformat

import json

from socialnetwork.models import *

# Create your views here.

@login_required
@ensure_csrf_cookie
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

@ensure_csrf_cookie
def add_comment_w_id(request, id):
    # if (request.user.id != id):
    #     return _my_json_error_response("incorrect user", status=400)
    return add_comment(request)

@ensure_csrf_cookie
def add_comment(request):
    if (not request.user.id):
        return _my_json_error_response("You must be logged in.", status=401)
    
    if (request.method == 'GET'):
        return _my_json_error_response("You must use a POST request for this operation", status=405)
    
    if (request.POST.get('comment_text', default=None) == None):
        return _my_json_error_response("missing needed comment_text field", status=400)

    if (request.POST.get('post_id', default=None) == None):
        return _my_json_error_response("missing needed post_id field", status=400)
    
    if (len(request.POST['comment_text']) == 0):
        return _my_json_error_response("You must input a comment to submit", status=400)

    if (len(request.POST['post_id']) == 0):
        return _my_json_error_response("There must be a post linked to each comment", status=400)
    
    if (not request.POST['post_id'].isnumeric()):
        return _my_json_error_response("Post ids should be numerical", status=400)
    
    if (int(request.POST['post_id']) > len(Post.objects.all())):
        return _my_json_error_response("invalid/nonexistent post_id", status=400)

    # if (request.POST['post_id'] > max(get_all_post_ids())):
    #     return _my_json_error_response("invalid/nonexistent post_id", status=400)
    
    new_comment = Comment(text=request.POST['comment_text'], 
                          creation_time=timezone.now(),
                          creator=request.user,
                          post=Post.objects.get(id=request.POST['post_id']))
    new_comment.save()
    new_commentJSON = {
            'id': new_comment.id,
            'text': new_comment.text,
            'post': new_comment.post.id,
            'creation_time': new_comment.creation_time.isoformat(),
            'creator': new_comment.creator.username,
            'userid': new_comment.creator.id,
            'first_name': new_comment.creator.first_name,
            'last_name': new_comment.creator.last_name
        }
    response_json = json.dumps(new_commentJSON)
    return HttpResponse(response_json, content_type='application/json')
    

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

@login_required
def get_follower_serialize(request):
    if (request.method == 'GET'):
        response_data = {}
        all_posts = []
        all_comments = []
        followings = request.user.profile.following.all()
        for post_item in Post.objects.all():
            if (post_item.user in followings):
                each_post = {
                    'id': post_item.id,
                    'text': post_item.text,
                    'user': post_item.user.username,
                    'userid': post_item.user.id,
                    'first_name': post_item.user.first_name,
                    'last_name': post_item.user.last_name,
                    'time': post_item.time.isoformat()
                }
                all_posts.append(each_post)
                for comment_item in Comment.objects.all():
                    if (comment_item.post.id == post_item.id):
                        each_comment = {
                        'id': comment_item.id,
                        'text': comment_item.text,
                        'post': comment_item.post.id,
                        'creation_time': comment_item.creation_time.isoformat(),
                        'creator': comment_item.creator.username,
                        'userid': comment_item.creator.id,
                        'first_name': comment_item.creator.first_name,
                        'last_name': comment_item.creator.last_name
                        }
                        all_comments.append(each_comment)
        response_data['posts'] = all_posts
        response_data['comments'] = all_comments
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type='application/json')


def get_global_comments_serializer(request):
    if (not request.user.id):
        return _my_json_error_response("You must be logged in.", status=401)
    response_data = {}
    all_posts = []
    for post_item in Post.objects.all():
        each_post = {
            'id': post_item.id,
            'text': post_item.text,
            'user': post_item.user.username,
            'userid': post_item.user.id,
            'first_name': post_item.user.first_name,
            'last_name': post_item.user.last_name,
            'time': post_item.time.isoformat()
        }
        all_posts.append(each_post)
    all_comments = []
    for comment_item in Comment.objects.all():
        each_comment = {
            'id': comment_item.id,
            'text': comment_item.text,
            'post': comment_item.post.id,
            'creation_time': comment_item.creation_time.isoformat(),
            'creator': comment_item.creator.username,
            'userid': comment_item.creator.id,
            'first_name': comment_item.creator.first_name,
            'last_name': comment_item.creator.last_name
        }
        all_comments.append(each_comment)
    response_data['posts'] = all_posts
    response_data['comments'] = all_comments
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

# def get_global_serializer(request):
#     response_data = []
#     for post_item in Post.objects.all():
#         each_post = {
#             'id': post_item.id,
#             'text': post_item.text,
#             'user': post_item.user.username,
#             'userid': post_item.user.id,
#             'first_name': post_item.user.first_name,
#             'last_name': post_item.user.last_name,
#             'time': post_item.time.isoformat()
#         }
#         response_data.append(each_post)
#     response_json = json.dumps(response_data)
#     return HttpResponse(response_json, content_type='application/json')


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
        print("got")
        user = get_object_or_404(User, id=id)
        context = {}
        context['profile'] = user.profile
        return render(request, 'socialnetwork/other.html', context)

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
    if (not request.user.id):
        return _my_json_error_response("You must be logged in.", status=401)

    if (request.method == 'GET'):
        return render(request, 'socialnetwork/global.html', { 'posts': Post.objects.all().order_by('time') })

    if 'text' not in request.POST or not request.POST['text']:
        context = { 'message': 'invalid text' }
        return render(request, 'socialnetwork/global.html', context)

    new_post = Post(text=request.POST['text'], user=request.user, time=timezone.now())
    
    new_post.save()
    return render(request, 'socialnetwork/global.html', { 'posts': Post.objects.all().order_by('time') })

@login_required
def follower_page(request):
    if (request.method == 'GET'):
        context = {}
        context['posts'] = Post.objects.all().order_by('-time')
        return render(request, 'socialnetwork/follower.html', context)