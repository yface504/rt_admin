from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #确保只有已登录的用户才能访问这些视图
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger #分页
from .models import Publisher
from django.conf import settings
import os



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
    success_files = []  # 存储成功上传的文件名

    if request.method == 'POST' and request.FILES.getlist('files'):
        uploaded_files = request.FILES.getlist('files')
        
        for uploaded_file in uploaded_files:
            # 检查上传文件的扩展名
            if uploaded_file.name.endswith(('.csv', '.xls', '.xlsx')):
                # 构建目标文件路径
                file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
                
                # 保存文件到目标路径
                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                # 记录成功上传的文件名
                success_files.append(uploaded_file.name)

    context = {"success_files": success_files}
    return render(request, 'update.html', context)