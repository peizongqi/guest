from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

# 发布会管理
@login_required()  #限制必须登录访问页面
def event_manage(request):
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {"user": username})  #读取cookies

# 登录逻辑
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 利用django自带的验证器进行帐号验证
        user = auth.authenticate(username=username, password=password)
        # if username == 'admin' and password == '123':
        if user is not None:
           auth.login(request, user)
           request.session['user'] = username  #添加浏览器cookies
           response = HttpResponseRedirect('/event_manage/')
           return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    else:
            return render(request, 'index.html', {'error': 'username or password error!'})
