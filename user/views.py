# Create your views here.
from django.shortcuts import render, redirect
from django.db.models import Q
from index.models import Dynamic
from user.models import *
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from user.forms import MyUserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 用户注册与登录
def loginView(request):
    # 表单对象user
    user = MyUserCreationForm()
    # 表单提交
    if request.method == 'POST':
        # 判断表单提交是     用户登陆     还是       用户注册
        # 用户登陆
        if request.POST.get('loginUser', ''):  # 获取搜索内容如果为loginUser，没有返回空
            loginUser = request.POST.get('loginUser', '')  # 这里是已经获取到用户输入的
            password = request.POST.get('password', '')
            if MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)):
                user = MyUser.objects.filter(
                    Q(mobile=loginUser) | Q(username=loginUser)).first()  # 这里是sql语句在django中的不同表示方法
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('/user/home/1.html')  # 页面跳转
                else:
                    tips = '密码错误'
            else:
                tips = '用户不存在'
        # 用户注册
        else:
            user = MyUserCreationForm(request.POST)
            if user.is_valid():
                user.save()
                tips = '注册成功'
            else:
                if user.errors.get('username', ''):
                    tips = user.errors.get('username', '注册失败')
                else:
                    tips = user.errors.get('mobile', '注册失败')
    return render(request, 'login.html', locals())


# 用户中心
# 设置用户登录限制
@login_required(login_url='/user/login.html')
def homeView(request, page):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 分页功能
    song_info = request.session.get('play_list', [])
    paginator = Paginator(song_info, 3)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', locals())


def logoutView(request):
    logout(request)
    return redirect('/')