import os
import datetime
from supabase import create_client, Client
from TaiwanLottery import TaiwanLotteryCrawler

# 獲取環境變量中的資訊
url = "https://diyprppuvnlwmrqylkqs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpeXBycHB1dm5sd21ycXlsa3FzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMzY1NDIxMiwiZXhwIjoyMDE5MjMwMjEyfQ.44N8-jaCH2XFBDeAKnGQxMjnOih-5nGduMfu6G7wQDA"

# 建立Supabase連接
supabase: Client = create_client(url, key)

# 從Supabase獲取最大日期
data = supabase.table('leto').select('date').order('date', desc=True).limit(1).execute()
max_date_str = data.data[0]['date']

# 處理時區信息，因為 Python 標準庫中的 fromisoformat 不能處理帶冒號的時區部分
if '+' in max_date_str:
    max_date_str = max_date_str.rsplit('+', 1)[0]  # 移除時區部分

# 使用 datetime.datetime.fromisoformat 正確處理日期時間字符串
max_date = datetime.datetime.fromisoformat(max_date_str)


# 獲取當前日期和最大日期的年份和月份
current_date = datetime.datetime.now(datetime.timezone.utc)
# 產生需要抓取的年份和月份列表
years_months = []
if (max_date.year == current_date.year and max_date.month == current_date.month):
    years_months.append(f"{max_date.year}-{str(max_date.month).zfill(2)}")
else:
    for year in range(max_date.year, current_date.year + 1):
        start_month = max_date.month if year == max_date.year else 1
        end_month = current_date.month if year == current_date.year else 12
        for month in range(start_month, end_month + 1):
            years_months.append(f"{year}-{str(month).zfill(2)}")

# 使用TaiwanLotteryCrawler抓取彩票資訊a
lottery = TaiwanLotteryCrawler()
for year_month in years_months:
    year, month = year_month.split('-')
    result = lottery.lotto649([year, month])
    print(result)

    # 篩選並記錄資料到Supabase
    for record in result:
        if datetime.datetime.fromisoformat(record['開獎日期']) > max_date:
            # 將資料結構轉換並寫入Supabase
            transformed = {
                'period': record['期別'],
                'date': record['開獎日期'],
                'ball_1': record['獎號'][0],
                'ball_2': record['獎號'][1],
                'ball_3': record['獎號'][2],
                'ball_4': record['獎號'][3],
                'ball_5': record['獎號'][4],
                'ball_6': record['獎號'][5],
                'ball_SP': record['特別號']
            }
            supabase.table('leto').insert(transformed).execute()