
import requests
from datetime import datetime
import pandas as pd

# 定義 API URL
url = "https://api.alternative.me/fng/"

# 發送 GET 請求獲取最新數據
response = requests.get(url, params={"limit": 1, "format": "json"})

if response.status_code == 200:
    data = response.json()
    if "data" in data and data["data"]:
        latest = data["data"][0]
        index = latest["value"]
        classification = latest["value_classification"]
        timestamp = datetime.utcfromtimestamp(int(latest["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Fear and Greed 指數: {index} ({classification})")
        print(f"數據時間: {timestamp}")
    else:
        print("無法獲取 Fear and Greed 指數數據。")
else:
    print(f"API 請求失敗，狀態碼: {response.status_code}")

# 發送請求，指定 limit 為較小的數字（例如10）
response = requests.get(url, params={"limit": 10, "format": "json"})

if response.status_code == 200:
    data = response.json()
    print("過去 10 天的 Fear and Greed 指數:")
    records = []
    for record in data["data"]:
        index = record["value"]
        classification = record["value_classification"]
        timestamp = datetime.utcfromtimestamp(int(record["timestamp"])).strftime('%Y-%m-%d')
        records.append([timestamp, index, classification])
    
    # 將數據保存為 DataFrame
    df = pd.DataFrame(records, columns=["Date", "Index", "Classification"])

    # 保存為 CSV 文件
    df.to_csv("fear_and_greed_index.csv", index=False, encoding="utf-8-sig")

    # 顯示 DataFrame
    print(df)
else:
    print(f"API 請求失敗，狀態碼: {response.status_code}")
