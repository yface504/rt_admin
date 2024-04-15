import pandas as pd

# 載入數據
mysql_data = pd.read_csv('E:\下載\cnt_logs.csv')
supabase_data = pd.read_csv('E:\下載\supa_id.csv')

# 使用 'id' 列進行比較，找出缺失的記錄
missing_records = mysql_data[~mysql_data['id'].isin(supabase_data['id'])]

# 顯示缺失的記錄數量
print(f"找到 {missing_records.shape[0]} 條缺失的記錄。")

# 保存缺失的記錄到一個新的 CSV 文件
missing_records.to_csv('E:\下載\supa.csv', index=False) # 請替換成希望保存的文件路徑
