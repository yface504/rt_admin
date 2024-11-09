import os
import re

# 讀取劇本.txt
input_file = r'E:\python\遊戲開發工具\劇本.txt'
output_file = r'E:\python\遊戲開發工具\轉換後劇本.txt'

# 替代文字對應表
replacement_dict = {
    "N": "？？？",
    "Z": "子晴",
    "A": "阿蜜莉雅",
    "WM": "白貓"
}

# 檢查檔案是否存在
if os.path.exists(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            line = line.strip()  # 去除每行首尾的空格和換行符

            # 如果該行是空行，則跳過處理
            if not line:
                continue
            
            # 檢查是否有對應的開頭文字
            match_found = False
            for key, value in replacement_dict.items():
                # 使用 re.escape 對 value 進行轉義，以避免特殊字符引發錯誤
                escaped_value = re.escape(value)
                
                # 使用正則表達式匹配開頭的文字（例如 "子晴："）
                if re.match(f'^{escaped_value}：', line):
                    # 將對應的代號替換到開頭，並刪除原本的名字部分
                    new_line = re.sub(f'^{escaped_value}：', f'{key} "', line)
                    new_line += '"'  # 補上結尾的引號
                    match_found = True
                    break
            
            if not match_found:
                # 如果沒有匹配到開頭文字，則直接將句子包裹在雙引號內
                new_line = f'"{line}"'
            
            # 將處理後的句子寫入新的文件
            file.write(new_line + '\n')

    print(f"轉換完成，結果已儲存至 {output_file}")

else:
    print(f"找不到檔案：{input_file}")
