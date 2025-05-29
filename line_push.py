import os
import requests
import random
import json

# 從 GitHub Actions 的 secrets 取得 TOKEN 與 USER ID
token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
user_id = os.environ['LINE_USER_ID']

# 讀取 GitHub 上的經文 json
res = requests.get("https://raw.githubusercontent.com/smallcisum/bible/main/bible.json")
quotes = res.json()

# 隨機選一句
quote = random.choice(quotes)
text = '\n'.join(quote) if isinstance(quote, list) else str(quote)

# 發送 LINE 訊息
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "to": user_id,
    "messages": [{"type": "text", "text": text}]
}

response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)

# 印出結果供 GitHub Actions 檢查
print("🔔 發送內容：", text)
print("📬 回應狀態：", response.status_code)
print("📦 LINE 回覆：", response.text)
