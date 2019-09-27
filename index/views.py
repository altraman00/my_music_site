from django.shortcuts import render

# Create your views here.
from index.models import *


def indexView(request):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:8]
    # 音乐分类
    label_list = Label.objects.all()
    # 热门歌曲
    play_hot_song = Dynamic.objects.select_related('song').order_by('-dynamic_plays').all()[:10]
    # 新歌推荐
    daily_recommendation = Song.objects.order_by('-song_release').all()[:5]
    # 热门搜索
    search_ranking = search_song[:6]
    # 热门下载
    down_ranking = Dynamic.objects.order_by('-dynamic_down').all()[:6]
    all_ranking = [search_ranking, down_ranking]
    # locals()可以直接将函数中所有变量全部传给模版
    return render(request, 'index.html', locals())


def page_not_found(request, exception):
    return render(request, 'error404.html', status=404)


def page_error(request):
    return render(request, 'error404.html', status=500)
