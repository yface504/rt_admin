from urllib import response
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import supabase_py

# 建立Supabase連接
url = "https://diyprppuvnlwmrqylkqs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpeXBycHB1dm5sd21ycXlsa3FzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMzY1NDIxMiwiZXhwIjoyMDE5MjMwMjEyfQ.44N8-jaCH2XFBDeAKnGQxMjnOih-5nGduMfu6G7wQDA"

supabase = supabase_py.create_client(url, key)

# 從Supabase獲取數據
response = supabase.table('leto').select('*').execute()

# 檢查是否有錯誤並處理數據
if 'error' in response:
    print("Error fetching data:", response['error'])
else:
    # 如果沒有錯誤，則從字典中取出數據
    data = response.get('data')
    if data:
        # 轉換數據為DataFrame
        df = pd.DataFrame(data)

        # 數據預處理
        df['date'] = pd.to_datetime(df['date'], utc=True)  # 處理帶有時區的日期

        # 特徵工程
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek

        # 分割數據為訓練集和測試集
        X = df[['month', 'day_of_week']]
        y = df[['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5', 'ball_6']]  # 以第一個球為例，可以重複此過程預測其它球號
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 建立模型
        models = {}
        for ball in y.columns:
            model = RandomForestClassifier(n_estimators=200, random_state=42)
            model.fit(X_train, y_train[ball])
            models[ball] = model

        # 預測測試集
        predictions = pd.DataFrame(columns=y.columns)
        for ball in y.columns:
            model = models[ball]
            predictions[ball] = model.predict(X_test)

        # 評估模型
        accuracies = {}
        for ball in y.columns:
            accuracy = accuracy_score(y_test[ball], predictions[ball])
            accuracies[ball] = accuracy
            print(f"Accuracy for {ball}: {accuracy}")

        # 使用模型預測未來的數據
        # day_of_week 星期二填1、星期五填4
        future_data = pd.DataFrame({'month': [9], 'day_of_week': [4]})
        future_predictions = pd.DataFrame(columns=y.columns)
        for ball in y.columns:
            model = models[ball]
            future_predictions[ball] = model.predict(future_data)

        print(f"\nFuture predictions for 2024-07-09:")
        print(future_predictions)

    else:
        print("No data available.")
