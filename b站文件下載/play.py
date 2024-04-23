import requests
from PIL import Image
from io import BytesIO



# 創建 session
session = requests.Session()

# 獲取驗證碼圖片
captcha_url = 'https://tv-cp.snm0516.aisee.tv/xapi/user/captcha?ts=0'
response = session.get(captcha_url)

print(response.headers['Content-Type'])

# 檢查 HTTP 響應是否成功
if response.status_code == 200:


    # 嘗試打開圖片
    image = Image.open(BytesIO(response.content))
    image.show()

    # 提示用戶輸入驗證碼
    captcha_code = input("請輸入驗證碼：")


    # 登錄資料
    login_url = 'https://tv-cp.snm0516.aisee.tv/xapi/user/login'
    login_data = {
                'username': 'Renta',
                'password': 'Renta&Bilibili Comics-2024',
                'captcha': captcha_code  # 使用用戶輸入的驗證碼
    }

    # 發送登錄請求
    login_response = session.post(login_url, data=login_data)

    # 檢查是否登錄成功
    if login_response.ok:
        print('登錄成功')
    else:
        print('登錄失敗', login_response.text)
else:
    print(f"錯誤: HTTP 請求失敗，狀態碼 {response.status_code}")


