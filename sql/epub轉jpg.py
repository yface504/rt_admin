import os
from ebooklib import epub
from PIL import Image
import io

# 設置根目錄
root_dir = r"I:\KADOKAWA"

# 遍歷根目錄下的所有子目錄和文件
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.epub'):
            epub_path = os.path.join(subdir, file)
            print(f'處理文件: {epub_path}')

            try:
                # 讀取EPUB文件
                book = epub.read_epub(epub_path)

                # 遍歷EPUB文件中的所有項目
                for item in book.get_items():
                    # 確保項目有media_type屬性，然後檢查是否為圖像
                    if hasattr(item, 'media_type') and item.media_type.startswith('image/'):
                        try:
                            # 使用Pillow打開圖像
                            image = Image.open(io.BytesIO(item.content))
                            # 構建輸出文件的完整路徑，將圖片保存為JPEG格式
                            output_file = os.path.join(subdir, os.path.splitext(item.get_name())[0] + '.jpg')
                            
                            # 確保保存圖片的目錄存在（處理可能的嵌套目錄）
                            os.makedirs(os.path.dirname(output_file), exist_ok=True)
                            
                            # 保存圖像為JPEG格式
                            image.save(output_file, 'JPEG')
                            print(f'保存圖像: {output_file}')
                        except Exception as e:
                            print(f'無法處理圖像 {item.get_name()}：{e}')
            except Exception as e:
                print(f'無法讀取EPUB文件 {epub_path}：{e}')

print('所有圖像提取並轉換完成。')
