"""musicsRecommend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('register/',views.register),#请求进入注册界面
    path('sign_in/',views.sign_in),#请求登录界面
    path('login/',views.login),  #进入登录界面输完账号密码之后判断密码是否正确
    path('usernameExist/',views.usernameExist),#判断此账号是否有重名
    path('addUserInformation/',views.addUserInformation),
    path('Recommendsong/',views.Recommendsong),
    path('test/',views.test),
    path('personCenter/',views.personCenter),
    path('hotSong/',views.hotSong),
    path('searchSong/',views.searchSong),#请求搜索歌曲的那个页面
    path('search/',views.search),#显示出搜索的歌曲
    path('addSongToCenter/',views.addSongToCenter),
    path('deleteSongFromCenter/',views.deleteSongFromCenter),
    path('exit/',views.exit)
]
