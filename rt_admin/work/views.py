from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #确保只有已登录的用户才能访问这些视图
from .models import Publisher
from django.conf import settings
import os

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
def paper(request):
    # 指定目录路径
    directory_path = os.path.join(settings.STATICFILES_DIRS[0], 'paper')  # 目录路径

    # 获取目录中的所有文件名
    file_names = [os.path.basename(file_path) for file_path in os.listdir(directory_path)]



    # 构建下载链接列表
    download_links = []
    for file_name in file_names:
        # 构建文件的完整路径
        file_path = os.path.join(directory_path, file_name)
    
        # 使用文件名作为链接文本，将文件路径添加到下载链接
        download_links.append(f'{file_name}')

    return render(request, 'paper.html',  {'download_links': download_links})