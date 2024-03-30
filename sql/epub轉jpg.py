import os
from ebooklib import epub
from PIL import Image
import io

# 替換成你的EPUB文件路徑
epub_path = r"C:\Users\even5\Desktop\20240319_TEST\04000000A17390100000\04000000A17390100000.epub"
# 設置圖片保存的目錄
output_dir = r"C:\Users\even5\Desktop\20240319_TEST\04000000A17390100000"

# 確保輸出目錄存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 讀取EPUB文件
book = epub.read_epub(epub_path)

# 遍歷EPUB文件中的所有項目
for item in book.get_items():
    # 確保項目有media_type屬性，然後檢查是否為圖像
    if hasattr(item, 'media_type') and item.media_type.startswith('image/'):
        # 使用Pillow打開圖像
        image = Image.open(io.BytesIO(item.content))
        # 構建輸出文件的完整路徑
        output_file = os.path.join(output_dir, os.path.splitext(item.get_name())[0] + '.jpg')
        
        # 確保保存圖片的目錄存在（處理可能的嵌套目錄）
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 保存圖像為JPEG格式
        image.save(output_file, 'JPEG')

print('圖像提取並轉換完成。')