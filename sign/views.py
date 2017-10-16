from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    return render(request, 'index.html')

# 发布会管理
@login_required()  #限制必须登录访问页面
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {"user": username, 'events': event_list})  #读取cookies

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

#  发布会名称搜索
@login_required()
def search_name(request):
    username = request.session.get('user', '')
    searchName = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=searchName)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#  嘉宾管理
@login_required()
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

#  签到页面
@login_required()
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})

# 签到动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error.'})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})

    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result})

#  退出登录
@login_required()
def logout(request):
    auth.logout(request)           #退出登录
    response = HttpResponseRedirect('/index/')
    return response
