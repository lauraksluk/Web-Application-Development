"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.global_page, name='home'),
    path('socialnetwork/login', views.login_page, name='login'),
    path('socialnetwork/register', views.register_page),
    path('global', views.global_page, name='global'),
    path('other/global', views.global_page, name='global'),
    path('new-post', views.global_page, name='new-post'),
    path('follower', views.follower_page, name='follower'),
    path('other/follower', views.follower_page, name='follower'),
    path('unfollow/follower', views.follower_page, name='follower'),
    path('follow/follower', views.follower_page, name='follower'),
    path('logout', views.logout_action),
    path('follow/logout', views.logout_action),
    path('unfollow/logout', views.logout_action),
    path('other/logout', views.logout_action),
    path('profile', views.profile_page, name='my-profile'),
    path('unfollow/profile', views.profile_page, name='my-profile'),
    path('follow/profile', views.profile_page, name='my-profile'),
    path('follow/global', views.global_page, name='global'),
    path('unfollow/global', views.global_page, name='global'),
    path('other/profile', views.profile_page, name='my-profile'),
    path('other/<int:id>', views.other_profile, name='other'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('follow/<int:id>', views.follow, name='follow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow')
]
