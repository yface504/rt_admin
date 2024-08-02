# 遍歷 E:\下載\Programs 內的子資料夾
# 每個子資料夾裡有
# 1、資料夾名為thum 內有 9s開頭的jpg
# 2、資料夾名含有_ 內有cover.jpg
# 如果不滿足上述條件，將子資料夾的檔名加載到E:\下載\Programs\logs.txt
# 如果滿足條件，將cover.jpg複製並取代9s開頭的jpg


import os
import shutil

# 設定根目錄路徑
root_dir = r'I:\快看\[ok]'
log_file = os.path.join(root_dir, 'logs.txt')

# 遍歷根目錄下的所有子資料夹
for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        # 檢查子資料夹是否符合條件
        thum_folder = os.path.join(folder_path, 'thum')
        has_thum = os.path.isdir(thum_folder) and any(f.startswith('9s') and f.endswith('.jpg') for f in os.listdir(thum_folder))
        
        has_cover = any('_' in subfolder and 'cover.jpg' in os.listdir(os.path.join(folder_path, subfolder)) for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder)))
        
        if has_thum and has_cover:
            # 符合條件，進行覆蓋操作
            cover_path = next(os.path.join(folder_path, subfolder, 'cover.jpg') for subfolder in os.listdir(folder_path) if '_' in subfolder and 'cover.jpg' in os.listdir(os.path.join(folder_path, subfolder)))
            # 覆蓋所有9s開頭的jpg文件
            for file in os.listdir(thum_folder):
                if file.startswith('9s') and file.endswith('.jpg'):
                    shutil.copy(cover_path, os.path.join(thum_folder, file))
        else:
            # 不符合條件，將資料夹名稱寫入日志文件
            with open(log_file, 'a', encoding='utf-8') as file:
                file.write(f'{folder}\n')

