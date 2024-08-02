# 重命名指定路徑下的所有資料夾，去除資料夾名稱中的特殊字符「？！」
import os
import re

def rename_folders(base_path):
    # 獲取基路徑下所有的資料夾
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        # 檢查是否為資料夾
        if os.path.isdir(folder_path):
            # 去除資料夾名中的特殊字符「？！」
            new_folder_name = re.sub(r'[?!]', '', folder_name)
            new_folder_path = os.path.join(base_path, new_folder_name)
            # 重命名資料夾
            os.rename(folder_path, new_folder_path)
            print(f"Renamed '{folder_name}' to '{new_folder_name}'")

# 指定你的基路徑
base_path = "I:\\KADOKAWA\\I Was a Sacrifice but Now I’m a Consort to a God -All the Princesses are Fluffy-"
rename_folders(base_path)
