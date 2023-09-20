from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #确保只有已登录的用户才能访问这些视图
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger #分页
from .models import Publisher


# Create your views here.




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        # 用authenticate判断用户名密码是否正确
        if user:
            login(request,user)
            return redirect('index')
        else:
            msg='帐密错误！'
            return render(request,'login.html',locals())
    return render(request,'login.html')

def log_out_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login') #redirect when user is not logged in
def index(request):
    user = request.user 
# 返回響應
    return render(request,'index.html', {'user': user})

@login_required(login_url='login')
def publisher(request):
    publishers = Publisher.objects.all()
    return render(request, 'publisher.html', {'publishers': publishers})


@login_required(login_url='login')
def update(request):
    pass
    return render(request,'update.html')