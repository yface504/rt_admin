import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from TaiwanLottery import TaiwanLotteryCrawler


# 確認當前工作目錄
print("Current working directory: ", os.getcwd())

# 如果當前工作目錄不是腳本所在目錄，設置工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("New working directory: ", os.getcwd())

# 定義API範圍
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 加載憑證
creds = ServiceAccountCredentials.from_json_keyfile_name("./coastal-haven-427921-b1-990d3e0f1055.json", scope)
client = gspread.authorize(creds)

# 打開Google Sheets
spreadsheet_id = "1wl7k2tmgsc6f-ZqLvMAz6Ga1SNKHk9eIRQ1-VU6zxQQ"
sheet = client.open_by_key(spreadsheet_id).sheet1

# 讀取數據
data = sheet.get_all_records()
# 將數據轉換為pandas DataFrame
df = pd.DataFrame(data)

# 尋找標題為“開獎日期”的列並獲取其最大日期
if '開獎日期' in df.columns:
    df['開獎日期'] = pd.to_datetime(df['開獎日期'], errors='coerce')  # 將列轉換為日期類型
    max_date = df['開獎日期'].max()  # 獲取最大日期
    print("最大開獎日期：", max_date)
else:
    print("找不到標題為“開獎日期”的列")

lottery = TaiwanLotteryCrawler()
result = lottery.lotto649()
print(result)

# 處理日期格式並過濾數據
for entry in result:
    entry['開獎日期'] = entry['開獎日期'].split('T')[0]

new_results = [entry for entry in result if pd.to_datetime(entry['開獎日期']) > max_date]

# 如果max_date為None，意味著沒有現有數據，將所有result作為新數據
if max_date is not None:
    new_results = [entry for entry in result if pd.to_datetime(entry['開獎日期']) > max_date]
else:
    new_results = result

# 檢查 new_results 是否為空
if not new_results:
    print("沒有新數據需要寫入")
else:
    # 將“獎號”數組拆成獨立的列
    processed_results = []
    for entry in new_results:
        processed_entry = {
            '期別': entry['期別'],
            '開獎日期': entry['開獎日期'],
            '獎號1': entry['獎號'][0],
            '獎號2': entry['獎號'][1],
            '獎號3': entry['獎號'][2],
            '獎號4': entry['獎號'][3],
            '獎號5': entry['獎號'][4],
            '獎號6': entry['獎號'][5],
            '特別號': entry['特別號']
        }
        processed_results.append(processed_entry)

    # 將數據寫入 Google Sheets
    df_new = pd.DataFrame(processed_results)
    sheet.append_rows(df_new.values.tolist(), value_input_option='USER_ENTERED')
    print("新數據已寫入Google Sheets")

    # 重新讀取所有數據
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # 將“開獎日期”列轉換為日期類型
    df['開獎日期'] = pd.to_datetime(df['開獎日期'], errors='coerce')

    # 按“開獎日期”從最新到最舊排序
    df = df.sort_values(by='開獎日期', ascending=False)

    # 將日期類型轉換回字符串以便寫入Google Sheets
    df['開獎日期'] = df['開獎日期'].dt.strftime('%Y-%m-%d')

    # 清空現有的sheet內容
    sheet.clear()

    # 重新寫入排序後的數據
    sheet.update([df.columns.values.tolist()] + df.values.tolist(), value_input_option='USER_ENTERED')


import webbrowser
url = "https://docs.google.com/spreadsheets/d/1wl7k2tmgsc6f-ZqLvMAz6Ga1SNKHk9eIRQ1-VU6zxQQ/edit?gid=0#gid=0"
webbrowser.open(url)
