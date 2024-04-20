import os
import pandas as pd

def is_skip_folder(folder_name):
    # 檢查文件夾名是否以數字和底線開頭
    return folder_name[0].isdigit() and '_' in folder_name

# 設定要查找的目錄
base_path = r'I:\快看\[ok]'

try:
    # 用來儲存找到的文件路徑
    found_files = []

    # 使用 os.walk 遍歷目錄
    for root, dirs, files in os.walk(base_path):
        # 過濾掉需要忽略的子目錄
        dirs[:] = [d for d in dirs if not is_skip_folder(d)]

        # 檢查當前目錄下的文件
        for file in files:
            if file == '0001.jpg':
                found_files.append(os.path.join(root, file))

    if not found_files:
        print("沒有找到名為 '0001.jpg' 的文件。")
    else:
        # 使用 pandas 創建 DataFrame
        df = pd.DataFrame(found_files, columns=['File Path'])
        # 將 DataFrame 保存到 Excel 文件中
        df.to_excel(r'E:\python\快看漫畫整理\found_files.xlsx', index=False)
        print("文件已保存到 'found_files.xlsx'。")

except Exception as e:
    print(f"無法訪問指定的目錄或執行查找，錯誤信息如下: {e}")
