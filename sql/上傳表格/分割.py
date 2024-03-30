import pandas as pd

# 假設您的CSV檔案路徑
csv_path = 'E:\\下載\\cnt_logs.csv'

# 讀取CSV檔案
df = pd.read_csv(csv_path)

# 計算分割點
split_index = len(df) // 2

# 分割DataFrame
df_first_half = df.iloc[:split_index]
df_second_half = df.iloc[split_index:]

# 定義儲存的檔案路徑
output_path_first_half = 'E:\\下載\\cnt_logs_part1.csv'
output_path_second_half = 'E:\\下載\\cnt_logs_part2.csv'

# 將分割後的資料分別儲存為兩個CSV檔案
df_first_half.to_csv(output_path_first_half, index=False)
df_second_half.to_csv(output_path_second_half, index=False)

print(f'已將檔案分割為兩部分，並分別儲存到 {output_path_first_half} 和 {output_path_second_half}')
