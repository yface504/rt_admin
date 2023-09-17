from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    pass
# 返回響應
    return render(request,'index.html')


def login(request):
    pass
# 返回響應
    return render(request,'login.html')