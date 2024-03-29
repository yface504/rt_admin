from django.shortcuts import render
from django.contrib.auth.decorators import login_required #确保只有已登录的用户才能访问这些视图
from .models import Publisher
from django.conf import settings
import os
import pandas as pd
import openpyxl

#載入匯率模塊
from datetime import datetime
import calendar
import requests
from bs4 import BeautifulSoup
from decimal import Decimal

#載入時間模塊
from datetime import datetime
import calendar


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
            
            # 如果文件名以"PAS"开头且以"jp"结尾，进行日本各家版稅結算
            if uploaded_file.name.startswith("PAS") and uploaded_file.name.endswith("jp.csv"):

                df = pd.read_csv(file_path, encoding='shift_jis')

                # 提取指定标题的列数据
                selected_columns = ['掲載日', '書名', '著者名', '価格', '当月合計冊数', '出版社名']
                df = df[selected_columns]

                # 删除'価格'列中值为0的行
                df = df[df['価格'] != 0]

                # 新增 'SalesAmount' 列
                df['SalesAmount'] = df['価格'] * df['当月合計冊数']
                selected_columns = ['掲載日', '書名', '著者名', '価格', '当月合計冊数', '出版社名', 'SalesAmount']


                SUMsales ='SalesAmount'
                Pname='出版社名'


                # 重置索引
                df = df.reset_index(drop=True)

                # 提取原文件名上的日期
                filename = os.path.splitext(os.path.basename(file_path))[0]

                # 找到 "A-" 和 "rnt" 在文件名中的索引
                start_index = filename.index("A-") + len("A-")
                end_index = filename.index("rnt")

                # 使用切片获取目标部分
                titleDate = filename[start_index:end_index]

                # 交由下列函數進行
                paper(df, selected_columns, SUMsales, titleDate, Pname)

                # 删除原始XLS或XLSX文件
                os.remove(file_path)

            # 如果文件名以"PAS"开头且以"en"结尾，进行美國各家版稅結算
            if uploaded_file.name.startswith("PAS") and uploaded_file.name.endswith("en.csv"):
                df = pd.read_csv(file_path, encoding='shift_jis')

                # 提取指定标题的列数据
                selected_columns = ['Release date','Title','Author','Price','Total sales (current month)','Publisher']
                df = df[selected_columns]

                # 删除'価格'列中值为0的行
                df = df[df['Total sales (current month)'] != 0]

                # 新增 'SalesAmount' 列
                df['SalesAmount'] = (df['Price'] * df['Total sales (current month)']).apply(Decimal)
                selected_columns = ['Release date','Title','Author','Price','Total sales (current month)','Publisher', 'SalesAmount']


                SUMsales ='SalesAmount'
                Pname='Publisher'


                # 重置索引
                df = df.reset_index(drop=True)

                # 提取原文件名上的日期
                filename = os.path.splitext(os.path.basename(file_path))[0]

                # 找到 "A-" 和 "rnt" 在文件名中的索引
                start_index = filename.index("A-") + len("A-")
                end_index = filename.index("rnt")

                # 使用切片获取目标部分
                titleDate = filename[start_index:end_index]

                # 交由下列函數進行
                paper(df, selected_columns, SUMsales, titleDate, Pname)

                # 删除原始XLS或XLSX文件
                os.remove(file_path)
            
            # 如果文件是XLS或XLSX，提取第二页，进行台灣各家版稅結算
            if uploaded_file.name.endswith(('.xls', '.xlsx')):

                # 读取Excel文件
                df = pd.read_excel(file_path, sheet_name=1) # sheet_name=1提取第二页
                # 提取原文件名上的日期
                titleDate = os.path.splitext(os.path.basename(file_path))[0].split('_')[0]

                selected_columns = ['系列書名', '集數', '出版社', '售價', '購買日期']
                SUMsales ='售價'
                Pname = '出版社'
        
                # 交由下列函數進行
                paper(df, selected_columns, SUMsales, titleDate, Pname)

                # 删除原始XLS或XLSX文件
                os.remove(file_path)
            
            # 记录成功上传的文件名
            success_files.append(uploaded_file.name)

    context = {"success_files": success_files}
    return render(request, 'update.html', context)

#處理報表
def paper(df, selected_columns, SUMsales, titleDate, Pname): #EXCEL轉成csv
    try:

        
        # 提取包含指定标题的列数据
        df = df[selected_columns]
        
        # 使用groupby按出版社名称分组
        grouped = df.groupby(Pname)

        for publisher_name, publisher_data in grouped:
            # 在这里，publisher_data 包含属于同一出版社的数据
            # 可以在每个出版社上应用你需要的操作
            # publisher_name 可以用于标识出版社

            # 计算"售價"列的总和
            total_sales = publisher_data[SUMsales].sum()

            # 将总和传递给 sum 变量
            sum = total_sales

            # 查询匹配的publisher数据
            publisher = Publisher.objects.filter(shelf_name=publisher_name).first()

            if publisher:
                # 提取需要的数据
                fees = publisher.fees_percentage
                ratio = publisher.ratio_percentage
                name = publisher.name
                area = publisher.area
                exchange_rate_method = publisher.exchange_rate_method

                # 获取映射值，如果 area 存在于 area_map 中，就获取映射值，否则使用默认值 'UNKNOWN'
                area_map = {
                    '台湾': 'TW',
                    '日本': 'JP',
                    '美国': 'EN',
                }
                area_code = area_map.get(area, 'UNKNOWN')

                # 构建新文件名
                new_file_name = f"{name}_{area_code}_{titleDate}"
                new_file_dir = os.path.join(settings.STATICFILES_DIRS[0], 'paper')  # 目录路径
                new_file_path = os.path.join(new_file_dir, new_file_name + '.xlsx')

                # 打开 sample.xlsx 文件，仅加载 report 工作表
                sample_file_path = os.path.abspath(os.path.join(settings.STATICFILES_DIRS[0], 'sample.xlsx'))
                sample_workbook = openpyxl.load_workbook(sample_file_path, data_only=True)
                srs = sample_workbook['report']

                # 调用 FindFxRate 函数，传递 area、exchange_rate_method 和 titleDate
                FxRate = FindFxRate(area, exchange_rate_method, titleDate)

                # 修改 report 工作表的特定单元格
                srs['B3'] = name #出版社名
                srs['F3'] = int(titleDate) #報表月            
                srs['A5'] = area_code
                srs['B5'] = FxRate
                srs['C5'] = sum
                srs['D5'] = fees #手續費
                srs['E5'] = ratio #拆帳比
                srs['F5'] = round(sum * (1 - fees) * ratio * FxRate, 2) #拆帳小計

                # 添加明细工作表
                new_sheet = sample_workbook.create_sheet("明細")

                # 将处理后的数据存放在 "明細" 中，首先添加列标题
                new_sheet.append(selected_columns)  # 添加列标题

                # 添加 DataFrame 中的数据行
                for _, row in publisher_data.iterrows():
                    new_sheet.append(row.tolist())

                # 创建新的.xlsx文件，将 sample.xlsx 另存为新路径和文件名
                new_sample_file_path = os.path.join(new_file_dir, new_file_path)
                sample_workbook.save(new_sample_file_path)

                print(f"已创建新的 '明細' 工作表并保存到新文件。")
            else:
                print(f"找不到匹配的Publisher数据。")
            
    except Exception as e:
        print(f"转换失败: {str(e)}")
    

# FindFxRate 查詢中國人民銀行外匯匯率
def FindFxRate(area, exchange_rate_method, titleDate):
    # ...（FindFxRate 函数的实现，包括计算 FxRate）
    # 字典 - 匯率方式映射到第幾張表格、關鍵字、公式
    area_rate = area + ',' + exchange_rate_method
    area_rate_map = {
        '台湾,中间价': (0, "新台币", lambda td_elements, keyword_position: (float(td_elements[keyword_position + 2].get_text()) + float(td_elements[keyword_position + 4].get_text())) / 200),
        '日本,中间价': (1, "100日元/人民币", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text()) / 100),
        '美国,中间价': (1, "美元/人民币", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text())),
        '日本,汇款买入价': (0, "日元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text()) / 100),
        '日本,汇款卖出价': (0, "日元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 4].get_text()) / 100),
        '美国,汇款买入价': (0, "美元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 1].get_text()) / 100),
        '美国,汇款卖出价': (0, "美元", lambda td_elements, keyword_position: float(td_elements[keyword_position + 4].get_text()) / 100)
    }

    # 將titleDate轉換為日期格式，設置為該月的最後一天
    new_date = datetime.strptime(titleDate+ '01', "%Y%m%d")
    last_day = datetime(new_date.year, new_date.month, calendar.monthrange(new_date.year, new_date.month)[1])

    # 构建 URL
    wocha = "https://chl.cn/?" + str(new_date.year) + "-" + str(new_date.month) + "-" + str(last_day.day)

    # 发送HTTP请求并获取页面内容
    response = requests.get(wocha)
    response.encoding = 'utf-8'  #改變頁面內容的編碼

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用Beautiful Soup解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取用户输入对应的映射数据
        table_index, keyword, formula = area_rate_map.get(area_rate, (None, None, None))

        if table_index is not None and keyword is not None and formula is not None:
            # 找到对应的表格元素
            tables = soup.find_all('table')
            target_table = tables[table_index]

            # 初始化关键字位置的变量
            keyword_position = None

            # 在整个表格中搜索关键字
            for i, td in enumerate(target_table.find_all('td')):
                # 如果关键字在<td>元素中
                if keyword in td.get_text():
                    keyword_position = i  # 记录关键字位置
                    break  # 找到后停止寻找

            if keyword_position is not None:
                print("关键字位置是表格的第", keyword_position, "个td")

                # 获取相应的数值并应用公式
                td_elements = target_table.find_all('td')
                result = formula(td_elements, keyword_position)

                # 外匯匯率小數點後6位
                FxRate = "{:.6f}".format(result)
                print("目標匯率:", FxRate)

                # 外匯匯率時間
                h1s = soup.find_all('h1')
                banktime = h1s[0].get_text()
                print("匯率時間:", banktime)
            else:
                print("未找到關鍵字")
        else:
            print("匯率方式為無，匯率以1計算")
            FxRate =1
    else:
        print("HTTP請求失敗，狀態碼:", response.status_code)
    FxRate = Decimal(FxRate)  # 将 FxRate 转换为 decimal.Decimal 类型
    return FxRate  # 返回 FxRate 的值