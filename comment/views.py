from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from index.models import *
import time
# Create your views here.


def commentView(request, song_id):
    # 搜索结果
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 提交评论处理
    if request.method == "POST":
        comment_text = request.POST.get('comment','')
        comment_user = request.user.username if request.user.username else '匿名用户'
        if comment_text:
            comment = Comment()
            comment.comment_text = comment_text
            comment.comment_user = comment_user
            comment.comment_date = time.strftime("%Y-%m-%d", time.localtime)
            comment.song_id = song_id
            comment.save()
        return redirect('/comment/%s.html'%(str(song_id)))
    else:
        song_info = Song.objects.filter(song_id=song_id).first()
        if not song_info:
            raise Http404
        comment_all = Comment.objects.filter(song_id=song_id).order_by('comment_date')
        song_name = song_info.song_name
        # 当请求参数不存在时，默认页数为1，如果存在，将参数值转化为整型
        page = int(request.GET.get('page', 1))
        # 每两条评论设置为一页
        paginator = Paginator(comment_all, 2)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'comment.html', locals())