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
    path('global', views.global_page),
    path('follower', views.follower_page),
    path('logout', views.logout_action),
    path('profile', views.profile_page, name='profile'),
    path('other', views.other_profile, name='other')
]
