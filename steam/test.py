import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta
import requests

# 載入環境變數
load_dotenv()
spreadsheet_id = os.getenv('STEAM')

# Google Sheets API 驗證
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"E:\python\steam\looker-studio-431016-dd72c78b4f8f.json", scope)
client = gspread.authorize(creds)

# 連接到 Google Sheets
sheet = client.open_by_key(spreadsheet_id).sheet1  # 替換成你的工作表名稱或索引

# API URL
url = "https://api.gamalytic.com/steam-games/list?fields=name,releaseDate,copiesSold,price,revenue,avgPlaytime,reviewScore,publisherClass,publishers,developers,id,steamId&limit=50&sub_genres=Sexual%20Content,Visual%20Novel&tags=Sexual%20Content,Visual%20Novel"

# 發送GET請求
response = requests.get(url)

# 檢查響應狀態碼
if response.status_code == 200:
    # 轉換JSON數據
    data = response.json()
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # 輸出結果並寫入 Google Sheets
    for item in data['result']:
        formatted_date = datetime.fromtimestamp(item['releaseDate'] / 1000, timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
        gamalytic = 'https://gamalytic.com/game/' + str(item['steamId'])
        steam = 'https://store.steampowered.com/app/' + str(item['steamId'])
        img = 'https://cdn.cloudflare.steamstatic.com/steam/apps/' + str(item['steamId']) + '/header.jpg'
        
        # 取得所有現有資料
        records = sheet.get_all_records()
        
        # 檢查是否有相同的日期和 steamId
        row_index = None
        for i, record in enumerate(records):
            existing_date = record['日期']
            existing_steam_id = record['steamId']
            if existing_date == today_date and existing_steam_id == item['steamId']:
                row_index = i + 2  # +2 是因為 sheet.get_all_records() 從第二行開始，而 Gspread 的行數從 1 開始
        
        # 資料行內容
        new_row = [
            today_date,
            item['steamId'],
            item['name'],
            formatted_date,
            item['copiesSold'],
            item['price'],
            item['revenue'],
            item['avgPlaytime'],
            item['reviewScore'],
            ','.join(item['publishers']),
            ','.join(item['developers']),
            gamalytic,
            steam,
            img
        ]
        
        if row_index:
            # 更新現有資料
            sheet.update(f'A{row_index}:N{row_index}', [new_row])
        else:
            # 添加新資料
            sheet.append_row(new_row)
else:
    print("請求失敗，狀態碼：", response.status_code)
