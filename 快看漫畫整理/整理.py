import os
import shutil
import re
import sys

# 先複製check上的 C ~ J 欄到 納品.txt
# 設定要檢查的目錄
hd = "I:/快看/[ok]"
#hd = "E:/下載/快看"

file_path = f'E:\python\快看漫畫整理\納品.txt'

def extract_info_from_line(line):
    parts = line.strip().split('\t')
    group_name = parts[7].strip()  # 分組名稱
    episode = parts[4].strip()  # 集數
    rule1 = parts[0].strip()  # 規則1
    rule2 = f"{parts[1]}_{parts[2].strip().strip()}"  # 規則2
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
    missing_episodes = []
    
    # 四位數.jpg的正則表達式
    non_compliant_files = []
    pattern = re.compile(r'^\d{4}\.jpg$')

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


    for group_name, episode, rule1, rule2, new_folder_name in info_list:
        group_path = os.path.join(directory, group_name)
        thum_path = os.path.join(group_path, 'thum')
        episode_path = os.path.join(thum_path, episode)

        # 檢查對應集數的文件或目錄是否存在
        if not os.path.exists(episode_path):
            missing_episodes.append((group_name, episode))
        else:
            # 檢查每個文件是否符合四位數.jpg的格式
            for file in os.listdir(episode_path):
                if not pattern.match(file):
                    non_compliant_files.append((group_name, episode, file))

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

    if missing_folders or missing_thum_folders or missing_files or missing_episodes or non_compliant_files:
        print("发现缺失项，程序终止。")
        if missing_folders:
            print("以下分組的資料夾不存在:", missing_folders)
        if missing_thum_folders:
            print("\n以下分組缺少thum資料夾:", missing_thum_folders)
        if missing_files:
            print("\n以下分組的thum資料夾內缺少jpg或tif檔案:", missing_files)
        if missing_episodes:
            print("\n以下分組的thum資料夾內缺少指定集數的文件或目錄:", missing_episodes)
        if non_compliant_files:
            for group, episode, file in non_compliant_files:
                print(f"{group},話數:{episode} 存在不符合四位數.jpg的文件: {file}")
        sys.exit(1)  # 使用非零值表示出错退出


info_list, unique_group_names, unique_new_folder_names, new_folder_to_group_map = read_and_extract_info(file_path)

process_folders(hd, unique_group_names, unique_new_folder_names, new_folder_to_group_map)


def perform_file_operations(directory, info_list):
    for group_name, episode, rule1, rule2, new_folder_name in info_list:
        group_path = os.path.join(directory, group_name)
        thum_path = os.path.join(group_path, 'thum')
        episode_path = os.path.join(thum_path, episode)


        # 檢查對應集數的文件或目錄是否存在
        if not os.path.exists(episode_path):
            print((group_name, episode))
        else:
            # 1. 每一個episode裡的文件名前面加上rule1_，例如0001.jpg變為1234_0001.jpg
            for file in os.listdir(episode_path):
                new_file_name = f"{rule1}_{file}"
                os.rename(os.path.join(episode_path, file), os.path.join(episode_path, new_file_name))

            # 2. 將9s-*.jpg和cover.tif複製到每一個episode裡
            for file in os.listdir(thum_path):
                if file.startswith('9s-') and file.endswith('.jpg') or file == 'cover.tif':
                    shutil.copy(os.path.join(thum_path, file), episode_path)

            # 3. 將每一個episode的名稱改為規則定義的名稱
            new_episode_path = os.path.join(thum_path, rule2)
            os.rename(episode_path, new_episode_path)

            # 4. 將所有的episode移動到new_folder_name
            new_folder_path = os.path.join(thum_path, new_folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            shutil.move(new_episode_path, new_folder_path)

    # 列出所有group_name的路徑
    for group_name in set(info[0] for info in info_list):
        print("已完成:",os.path.join(new_folder_path))
perform_file_operations(hd, info_list)
