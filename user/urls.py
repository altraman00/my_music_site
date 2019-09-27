# -*- coding: utf-8 -*-
'''
Created by admin at 2019-07-28  
desc:
'''

from django.urls import path
from user import views


urlpatterns = [
    path('login.html', views.loginView, name='login'),
    path('home/<int:page>.html', views.homeView, name='home'),
    path('logout.html', views.logoutView, name='logout'),
]