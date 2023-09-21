from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #确保只有已登录的用户才能访问这些视图
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger #分页
from .models import Publisher
from django.conf import settings
import os
import codecs
from django.http import HttpResponse
import openpyxl
import csv
import pandas as pd

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



def convert_shift_jis_to_utf8(file_path): #SHIFT_JIS编码转换为UTF-8编码
    try:
        # 读取SHIFT_JIS编码的文件
        with codecs.open(file_path, 'r', encoding='shift_jis') as source_file:
            content = source_file.read()

        # 转换为UTF-8编码
        content_utf8 = content.encode('utf-8')

        # 保存文件以UTF-8编码
        with codecs.open(file_path, 'wb') as target_file:
            target_file.write(content_utf8)

        print(f"文件已成功从SHIFT_JIS编码转换为UTF-8编码。")

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 提取指定标题的列数据
        selected_columns = ['掲載日','書名','著者名','価格','当月合計冊数','出版社名']
        df = df[selected_columns]

        # 删除'価格'列中值为0的行
        df = df[df['価格'] != 0]

        # 重置索引
        df = df.reset_index(drop=True)

        # 将处理后的数据保存回原始的CSV文件（替换原文件）
        df.to_csv(file_path, index=False, encoding='utf-8')

        print("指定标题的列数据已提取并删除'価格'为0的数据，并保存回原始的CSV文件。")
    except Exception as e:
        print(f"处理失败: {str(e)}")

def convert_en(file_path):
    try:
        # 读取SHIFT_JIS编码的文件
        with codecs.open(file_path, 'r', encoding='shift_jis') as source_file:
            content = source_file.read()

        # 转换为UTF-8编码
        content_utf8 = content.encode('utf-8')

        # 保存文件以UTF-8编码
        with codecs.open(file_path, 'wb') as target_file:
            target_file.write(content_utf8)

        print(f"文件已成功从SHIFT_JIS编码转换为UTF-8编码。")

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 提取指定标题的列数据
        selected_columns = ['Release date','Title','Author','Price','Total sales (current month)','Publisher']
        df = df[selected_columns]

        # 删除'価格'列中值为0的行
        df = df[df['Total sales (current month)'] != 0]

        # 重置索引
        df.to_csv(file_path, index=False, encoding='utf-8')

        # 将处理后的数据保存回原始的CSV文件（替换原文件）
        df.to_csv(file_path, index=False)

        print("指定标题的列数据已提取并删除'Price'为0的数据，并保存回原始的CSV文件。")
    except Exception as e:
        print(f"处理en失败: {str(e)}")

def convert_xlsx_sheet_to_csv(xlsx_file_path, sheet_index, output_csv_file_path): #EXCEL轉成csv
    try:
        # 读取Excel文件
        df = pd.read_excel(xlsx_file_path, sheet_name=sheet_index)
        
        # 提取包含指定标题的列数据
        selected_columns = ['系列書名', '集數', '出版社', '售價', '購買日期']
        df = df[selected_columns]
        
        # 将数据保存为CSV文件
        df.to_csv(output_csv_file_path, index=False, encoding='utf-8')
        
        print(f"第{sheet_index + 1}页已成功提取指定列数据并转换为CSV文件。")
    except Exception as e:
        print(f"转换失败: {str(e)}")

@login_required(login_url='login')
def update(request):
    success_files = []  # 存储成功上传的文件名

    if request.method == 'POST' and request.FILES.getlist('files'):
        uploaded_files = request.FILES.getlist('files')
        
        for uploaded_file in uploaded_files:
            # 构建目标文件路径
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            
            # 保存文件到目标路径
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # 如果文件名以"PAS"开头且以"jp"结尾，进行编码转换
            if uploaded_file.name.startswith("PAS") and uploaded_file.name.endswith("jp.csv"):
                # 调用编码转换函数
                convert_shift_jis_to_utf8(file_path)

            # 如果文件名以"PAS"开头且以"jp"结尾，进行编码转换
            if uploaded_file.name.startswith("PAS") and uploaded_file.name.endswith("en.csv"):
                # 调用编码转换函数
                convert_en(file_path)
            
            # 如果文件是XLS或XLSX，提取第二页并将其转换为CSV文件
            if uploaded_file.name.endswith(('.xls', '.xlsx')):
                # 提取第二页并将其转换为CSV文件
                sheet_index_to_convert = 1  # 第二页的索引为1
                output_csv_file_path = os.path.splitext(file_path)[0]+ '.csv'
                convert_xlsx_sheet_to_csv(file_path, sheet_index_to_convert, output_csv_file_path)
                
                # 删除原始XLS或XLSX文件
                os.remove(file_path)
            
            # 记录成功上传的文件名
            success_files.append(uploaded_file.name)

    context = {"success_files": success_files}
    return render(request, 'update.html', context)


@login_required(login_url='login')
def paper(request):
    return render(request, 'paper.html')