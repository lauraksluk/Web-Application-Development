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
    path('socialnetwork/get-global', views.get_global_comments_serializer, name="get-global"),
    path('get-global', views.get_global_comments_serializer, name="get-global"),
    path('get-follower', views.get_follower_serialize, name="get-follower"),
    path('socialnetwork/get-follower', views.get_follower_serialize, name="get-follower"),
    path('socialnetwork/add-comment', views.add_comment, name='add-comment'),
    path('socialnetwork/add-comment-id/<int:id>', views.add_comment_w_id, name='add-comment-w-id'),
    path('add-comment/<int:id>', views.add_comment_w_id, name='add-comment-w-id'),
    path('socialnetwork/login', views.login_page, name='login'),
    path('socialnetwork/register', views.register_page, name='register'),
    path('socialnetwork/global', views.global_page, name='global'),
    path('global', views.global_page, name='global'),
    path('new-post', views.global_page, name='new-post'),
    path('socialnetwork/follower', views.follower_page, name='follower'),
    path('follower', views.follower_page, name='follower'),
    #path('unfollow/follower', views.follower_page, name='follower'),
    #path('follow/follower', views.follower_page, name='follower'),
    path('socialnetwork/logout', views.logout_action, name='logout'),
    path('logout', views.logout_action),
    path('follow/logout', views.logout_action),
    path('unfollow/logout', views.logout_action),
    path('other/logout', views.logout_action),
    path('socialnetwork/profile', views.profile_page, name='profile'),
    path('profile', views.profile_page, name='profile'),
    #path('follow/profile', views.profile_page, name='profile'),
    #path('follow/global', views.global_page, name='global'),
    #path('unfollow/global', views.global_page, name='global'),
    path('other/profile', views.profile_page),
    path('socialnetwork/other/<int:id>', views.other_profile, name='other'),
    path('other/<int:id>', views.other_profile, name='other'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('socialnetwork/follow/<int:id>', views.follow, name='follow'),
    path('socialnetwork/unfollow/<int:id>', views.unfollow, name='unfollow')
]
