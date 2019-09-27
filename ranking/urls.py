# -*- coding: utf-8 -*-
'''
Created by admin at 2019-07-28  
desc:
'''

from django.urls import path
from . import views


urlpatterns = [
    path('', views.rankingView, name='ranking'),
    path('.list', views.RankingList.as_view(), name='rankingList'),
]