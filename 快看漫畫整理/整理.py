import os
import shutil

# 設定要檢查的目錄
#hd = "I:/快看/[ok]"
hd = "E:/下載/快看"

def extract_info_from_line(line):
    parts = line.strip().split('\t')
    group_name = parts[7].strip()  # 分組名稱
    episode = parts[4].strip()  # 集數
    rule1 = parts[0].strip()  # 規則1
    rule2 = parts[1].strip()  # 規則2
    index_of_bracket = parts[2].find('[')
    new_folder_name = f"{parts[0].strip()}_{parts[2][:index_of_bracket].strip()}"
    return group_name, episode, rule1, rule2, new_folder_name

def merge_folders(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    for item in os.listdir(source):
        s_item = os.path.join(source, item)
        d_item = os.path.join(destination, item)

        if os.path.isdir(s_item):
            if not os.path.exists(d_item):
                os.makedirs(d_item)
            merge_folders(s_item, d_item)
        else:
            shutil.move(s_item, d_item)
    
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

def read_and_extract_info(file_path):
    unique_group_names = set()
    unique_new_folder_names = set()
    new_folder_to_group_map = {}
    info_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                group_name, episode, rule1, rule2, new_folder_name = extract_info_from_line(line)
  
                unique_group_names.add(group_name)
                unique_new_folder_names.add(new_folder_name)
                new_folder_to_group_map[new_folder_name] = group_name 
                info_list.append((group_name, episode, rule1, rule2, new_folder_name))
    
    return info_list, unique_group_names, unique_new_folder_names, new_folder_to_group_map

def process_folders(directory, unique_group_names, unique_new_folder_names, new_folder_to_group_map):
    missing_folders = []
    missing_thum_folders = []
    missing_files = []

    for group_name in unique_group_names:
        group_path = os.path.join(directory, group_name)
        
        if not os.path.exists(group_path):
            missing_folders.append(group_name)
        else:
            thum_path = os.path.join(group_path, 'thum')
            if not os.path.exists(thum_path):
                missing_thum_folders.append(group_name)
            else:
                has_jpg = any(file.endswith('.jpg') for file in os.listdir(thum_path))
                has_tif = any(file.endswith('.tif') for file in os.listdir(thum_path))
                if not (has_jpg and has_tif):
                    missing_files.append(group_name)

    for new_folder_name in unique_new_folder_names:
        group_name = new_folder_to_group_map[new_folder_name]
        group_path = os.path.join(directory, group_name)
        thum_path = os.path.join(group_path, 'thum')
        thum_new_folder_path = os.path.join(thum_path, new_folder_name)
        group_new_folder_path = os.path.join(group_path, new_folder_name)

        if not os.path.exists(thum_path):
            os.makedirs(thum_path)

        if os.path.exists(thum_new_folder_path):
            if not os.path.exists(group_new_folder_path):
                os.makedirs(group_new_folder_path)
            merge_folders(thum_new_folder_path, group_new_folder_path)
            shutil.rmtree(thum_new_folder_path)
            os.makedirs(thum_new_folder_path)


    if missing_folders:
        print("以下分組的資料夾不存在:", missing_folders)
    if missing_thum_folders:
        print("\n以下分組缺少thum資料夾:", missing_thum_folders)
    if missing_files:
        print("\n以下分組的thum資料夾內缺少jpg或tif檔案:", missing_files)

file_path = f'E:\python\快看漫畫整理\納品.txt'
info_list, unique_group_names, unique_new_folder_names, new_folder_to_group_map = read_and_extract_info(file_path)
process_folders(hd, unique_group_names, unique_new_folder_names, new_folder_to_group_map)

