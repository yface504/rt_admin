from django.shortcuts import render
from .models import Publisher
# Create your views here.

def index(request):
    pass
# 返回響應
    return render(request,'index.html')


def login(request):
    pass
# 返回響應
    return render(request,'login.html')

def publisher(request):
    publishers = Publisher.objects.all()
    return render(request, 'publisher.html', {'publishers': publishers})