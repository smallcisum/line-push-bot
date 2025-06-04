import requests
import json
import random
import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

# === LINE 設定 ===
CHANNEL_ACCESS_TOKEN = 'NFutE++FSNU/qXNjdTz9eaAnfBGQSLMDD+W/DFg7LuCiIvzc9i0IxgMahJigyF9gzPfKdTHcQJfrDh2glPLJeiOeOOsD6tEV9GwKGscFaolDao1pmiuZVSf+nWhKJsoqLLxMjK1KxXWfenBqbyGKEAdB04t89/1O/w1cDnyilFU='
USER_ID = 'Ua1ee40b62de1333b9f167cb4cf5d33f7'

# === 語錄來源 ===
BIBLE_JSON_URL = 'https://raw.githubusercontent.com/smallcisum/bible/main/bible.json'

app = Flask(__name__)

# === 每日推播函數 ===
def push_daily_quote():
    try:
        res = requests.get(BIBLE_JSON_URL)
        quotes = json.loads(res.text)
        quote = random.choice(quotes)
        text = '\n'.join(quote) if isinstance(quote, list) else str(quote)

        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        body = {
            "to": USER_ID,
            "messages": [{
                "type": "text",
                "text": f"📖 今日金句：\n{text}"
            }]
        }

        r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(body))
        
        # === Debug 輸出 ===
        print("LINE 回應狀態碼：", r.status_code)
        print("LINE 回應內容：", r.text)
        print("✅ 推播成功" if r.status_code == 200 else "⚠️ 推播失敗")

    except Exception as e:
        print("🚨 發生錯誤：", e)

# === 每日定時排程（中午 12:00 台北時間）===
scheduler = BackgroundScheduler(timezone='Asia/Taipei')
scheduler.add_job(push_daily_quote, 'cron', hour=12, minute=0)
scheduler.start()

# === 網頁路由 ===
@app.route('/')
def index():
    return '💌 金句推播機器人執行中！'

@app.route('/send')
def manual_send():
    push_daily_quote()
    return '📨 金句發送成功！'

# === 執行 Flask App ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
