import os
import shutil

# 設定要檢查的目錄
# hd = "I:/快看/[ok]"
hd = "E:/下載/快看"

# 讀取納品.txt文件並提取分組名稱
def extract_info_from_line(line):
    parts = line.strip().split('\t')
    group_name = parts[7].strip()  # 分組名稱
    episode = parts[4].strip()  # 集數
    rule1 = parts[8].strip()  # 規則1
    rule2 = parts[9].strip()  # 規則2
    new_folder_name = f"{parts[0].strip()}_{parts[2].split(' ')[0]}"  # 新資料夾名稱
    return group_name, episode, rule1, rule2, new_folder_name

def read_and_extract_info(file_path):
    info_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # 忽略空行
                info = extract_info_from_line(line)
                info_list.append(info)
    return info_list

def process_folders(info_list, directory):
    missing_folders = []
    missing_thum_folders = []
    missing_files = []

    for group_name, episode, rule1, rule2, new_folder_name in info_list:
        group_path = os.path.join(directory, group_name)
        
        # 檢查分組資料夾是否存在
        if not os.path.exists(group_path):
            missing_folders.append(group_name)
            continue
        
        # 檢查 thum 資料夾是否存在
        thum_path = os.path.join(group_path, 'thum')
        if not os.path.exists(thum_path):
            missing_thum_folders.append(group_name)
            continue

        # 檢查 thum 資料夾內是否有 jpg 和 tif 檔案
        has_jpg = any(file.endswith('.jpg') for file in os.listdir(thum_path))
        has_tif = any(file.endswith('.tif') for file in os.listdir(thum_path))
        if not (has_jpg and has_tif):
            missing_files.append(group_name)

        # 檢查並處理新資料夾
        new_folder_path = os.path.join(group_path, new_folder_name)
        if os.path.exists(new_folder_path):
            print(f"資料夾已正確位置：{new_folder_name}")
        else:
            temp_path = os.path.join(group_path, 'temp', new_folder_name)
            if os.path.exists(temp_path):
                shutil.move(temp_path, group_path)
                print(f"已從temp移動資料夾：{new_folder_name}")

    # 打印缺少的資料夾信息
    if missing_folders:
        print("以下分組的資料夾不存在:", missing_folders)
    if missing_thum_folders:
        print("\n以下分組缺少thum資料夾:", missing_thum_folders)
    if missing_files:
        print("\n以下分組的thum資料夾內缺少jpg或tif檔案:", missing_files)

file_path = './納品.txt'
info_list = read_and_extract_info(file_path)
process_folders(info_list, hd)