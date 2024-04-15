# def check_csv_for_malformed_quotes(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
        
#         for line_number, line in enumerate(lines, start=1):
#             # 計算每行中雙引號的數量
#             quote_count = line.count('"')
            
#             # 如果雙引號的數量是奇數，則認為這行有問題
#             if quote_count % 2 != 0:
#                 print(f"問題在第 {line_number} 行: 引號數量不匹配。")
#                 print(line)
#                 print("---")

# # 替換 'your_file.csv' 為您的 CSV 文件名
# check_csv_for_malformed_quotes("E:\下載\member_action_stats.csv")

import csv

def check_and_fix_csv_quotes(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            fixed_row = []
            for field in row:
                # 確保每個字段內的引號正確配對，修正單獨的引號問題
                fixed_field = field.replace('""', '"')  # 首先將雙引號替換為單引號（如果需要）
                if fixed_field.count('"') % 2 != 0:  # 如果引號數量為奇數
                    fixed_field = fixed_field.replace('"', '')  # 移除所有引號
                fixed_row.append(fixed_field)
            writer.writerow(fixed_row)

# 指定原始 CSV 文件和要寫入的新 CSV 文件的路徑
input_file_path = 'E:\下載\member_action_stats.csv'
output_file_path = 'E:\\下載\\fixed.csv'

# 執行檢查和修正
check_and_fix_csv_quotes(input_file_path, output_file_path)
