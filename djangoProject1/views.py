import time

from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect
from django_user_agents.utils import get_user_agent   #安装pip install django-user-agents

from djangoProject1 import models
from djangoProject1.forms import *
from djangoProject1.mail import *

def register(request):
    user_agent = get_user_agent(request)  # 获取设备类型
    if(user_agent.is_mobile):
        return render(request, 'register_m.html')
    return render(request, 'register.html')


def register_verify(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        print(register_form.is_valid())
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.cv=register_form.cleaned_data['cv']
                new_user.nick_name = 'NewPatentmapUser'
                new_user.region = '未设置'
                new_user.profile = '无个人简介'
                new_user.save()
                new_image = models.Image.objects.create()
                new_image.name = new_user.name
                new_image.image = '未设置头像'
                new_image.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())

def m_code(request):
    return render(request, 'login_m_code.html', locals())


def login(request):
    if request.session.get('is_login', None):
        if request.session.get('rememberMe', None):
            return redirect('/personal')
    if request.method == "POST":
        print('POST')
        rememberMe = request.POST.getlist('rememberMe')
        if (rememberMe == ['on']):
            request.session['rememberMe'] = True
        if request.session.get('is_login', None):
            if request.session.get('rememberMe', None):
                return redirect('/personal')              # 若检测到已登录则直接跳转
        form_id = request.POST.get('form_id')
        print(request.POST)
        print(form_id)
        if(form_id=="casLoginForm"):
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                try:
                    user = models.User.objects.get(name=username)
                    if user.password == password:
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name      #session记录用户登陆状态，便于之后在个人中心显示内容以及登出
                        return redirect('/personal/')
                    else:
                        message = "密码错误（Wrong Password）"
                except:
                    message = "用户不存在（Invalid User）"
            return render(request, 'login.html', locals())
        if(form_id=="casDynamicLoginForm"):
            initial_data = {'email': request.POST['email'], 'dynamicCode': request.POST['dynamicCode']}
            temp=QueryDict('', mutable=True)
            temp.update(initial_data)
            login_form = LoginFormEmail(temp)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                dynamicCode = login_form.cleaned_data['dynamicCode']
                try:
                    user = models.User.objects.get(email=email)
                    if email == request.session['email'] and dynamicCode==request.session['dynamic_code']:
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name  # session记录用户登陆状态，便于之后在个人中心显示内容以及登出
                        return redirect('/personal/')
                    else:
                        message = "动态码错误（Wrong code）"
                except:
                    message = "动态码过期，请重试"
            else:
                print(login_form.errors)
            return render(request, 'login.html', locals())
    login_form = LoginForm()
    user_agent = get_user_agent(request)  # 获取设备类型
    if user_agent.is_mobile:
        return render(request, 'login_m.html', locals())
    else:
        return render(request, 'login.html', locals())



def personal(request):
    session_name=request.session.get('user_name')
    user_data = models.User.objects.get(name=session_name)
    images = models.Image.objects.get(name=session_name)
    return render(request, 'personal.html', {"user_data": user_data}) #从数据库取东西显示到网页可以在这里实现


def personal_logout(request):
    request.session.flush()    #清空session
    return redirect("/login/")


def send_code(request):
    if request.method == "POST":
        email1 = request.POST.get("email")
        print(email1)
        try:
            user = models.User.objects.get(email=email1)
            print(user)
        except models.User.DoesNotExist:
            return JsonResponse('User does not exist')
        s_stat, code =send_sms_code(email1)
        if(s_stat==False):
            return JsonResponse('send failed, retry later')
        request.session['email'] = email1
        request.session['dynamic_code'] = code
        return JsonResponse({"msg": "success"})

def send_pwd(request):
    print("找回密码")
    if request.method == "POST":
        email1 = request.POST.get("email")
        print(email1)
        try:
            user = models.User.objects.get(email=email1)
            print(user)
        except models.User.DoesNotExist:
            return JsonResponse('User does not exist')
        s_stat = send_sms_pwd(user)
        if (s_stat == False):
            return JsonResponse('send failed, retry later')
        request.session['email'] = email1
        return redirect("/login/")

def personal_edit(request):
    session_name = request.session.get('user_name')
    user_data = models.User.objects.get(name=session_name)
    images = models.Image.objects.get(name=session_name)
    if request.method == "POST":
        nick_name = request.POST.get("nick_name","")
        email = request.POST.get("email","")
        cv = request.POST.get("cv","")
        sex = request.POST.get("sex","")
        region = request.POST.get("region","")
        profile = request.POST.get("profile","")
        if nick_name != "":
            user_data.nick_name = nick_name
        if email != "":
            user_data.email = email
        if cv != "":
            user_data.cv = cv
        if sex != "":
            user_data.sex = sex
        if region != "":
            user_data.region = region
        if profile != "":
            user_data.profile = profile
        user_data.save()

    return render(request, 'personal_edit.html', {"user_data": user_data})


def image(request):
    if request.method == 'GET':
        return render(request, 'personal_edit.html')
    if request.method == 'POST':
        name = request.session.get('user_name')
        image = request.FILES.get('image')
        same_name = models.Image.objects.filter(name=name)
        if same_name:
            models.Image.objects.get(name=name).delete()
        models.Image.objects.create(name = name,image = image)
        images = models.Image.objects.get(name=name)
        return render(request, 'personal_edit.html', {"images": images})


