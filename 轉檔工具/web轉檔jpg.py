import os
from PIL import Image

def convert_webp_to_jpg(directory):
    # 遍歷指定目錄及其所有子目錄
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.webp'):
                # 構建完整的文件路徑    
                webp_path = os.path.join(root, file)
                # 設置輸出的 JPG 文件路徑
                jpg_path = os.path.splitext(webp_path)[0] + '.jpg'
                
                # 開啟 WEBP 文件並轉換成 JPG
                with Image.open(webp_path) as img:
                    img.convert('RGB').save(jpg_path, 'JPEG')
                    
                print(f'Converted {webp_path} to {jpg_path}')

# 設置你的目錄路徑
directory_path = 'E:\下載\Hope'
convert_webp_to_jpg(directory_path)
