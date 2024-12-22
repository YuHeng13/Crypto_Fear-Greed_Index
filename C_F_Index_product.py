import requests
from datetime import datetime
import pandas as pd


def fetch_fear_and_greed(limit=1, format="json", date_format=""):
    """
    從 Alternative.me 的 API 獲取 Fear and Greed 指數數據。
    
    :param limit: 返回的數據條數，默認為 1 (最新數據)。
    :param format: 數據格式，可選 "json" 或 "csv"，默認為 "json"。
    :param date_format: 日期格式，可選 "us"、"cn"、"kr" 或 "world"。
    :return: 返回處理好的數據，或者錯誤信息。
    """
    url = "https://api.alternative.me/fng/"
    params = {
        "limit": 0,
        "format": format,
        "date_format": date_format
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果狀態碼不是 200，拋出錯誤
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_data(data):
    """
    顯示 Fear and Greed 指數數據。
    :param data: 從 API 獲取的數據 (JSON 格式)。
    """
    if "error" in data:
        print("Error:", data["error"])
        return

    print("=== Fear and Greed 指數數據 ===")
    for record in data.get("data", []):
        index = record["value"]
        classification = record["value_classification"]
        timestamp = datetime.utcfromtimestamp(int(record["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')
        print(f"日期: {timestamp} | 指數: {index} ({classification})")

# 主函數
if __name__ == "__main__":
    # 獲取最新 Fear and Greed 指數
    result = fetch_fear_and_greed(limit=1, format="json")
    display_data(result)
    
    print("\n=== 過去 10 天的數據 ===")
    # 獲取過去 10 天的 Fear and Greed 指數
    result = fetch_fear_and_greed(limit=10, format="json")
    display_data(result)
    
    
# 提取 data 並忽略其他鍵
data = result.pop("data", [])  # pop 可以安全地取出鍵，且刪除它

# 將 data 轉換為 DataFrame
df = pd.DataFrame(data)

# 刪除 "time_until_update" 欄位
df.drop(columns=["time_until_update"], inplace=True)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

# 將 DataFrame 儲存為 CSV 檔
df.to_csv("Crypto_Fear &Greed_Index.csv", index=False, encoding="utf-8-sig")

#查看數值獨特性
df.apply(lambda x:len(x.unique()))


