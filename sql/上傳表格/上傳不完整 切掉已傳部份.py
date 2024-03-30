import pandas as pd

# 假設你的原始CSV檔案路徑是 'E:\\下載\\sales_logs.csv'
input_csv_path = 'E:\\下載\\sales_logs.csv'

# 讀取CSV檔案
df = pd.read_csv(input_csv_path)

# 刪除id小於或等於53076192的資料
df_filtered = df[df['id'] > 53076192]

# 指定新CSV檔案的儲存路徑
output_csv_path = 'E:\\下載\\sales_logs2.csv'

# 將過濾後的資料寫入新的CSV檔案，不儲存索引列
df_filtered.to_csv(output_csv_path, index=False)

print(f'已將過濾後的資料儲存到 {output_csv_path}')
