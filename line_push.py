import requests
import json
import random
import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

# === LINE 設定 ===
CHANNEL_ACCESS_TOKEN = 'e6e267f4ffc2be6d9e79e45cc15e0ab2'
USER_ID = 'Ua1ee40b62de1333b9f167cb4cf5d33f7'

# === 語錄來源（妳的 GitHub JSON）===
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
        print("✅ 推播成功" if r.status_code == 200 else f"⚠️ 推播失敗：{r.status_code}")

    except Exception as e:
        print("發生錯誤：", e)

# === 每日定時排程（中午 12:00 台北時間）===
scheduler = BackgroundScheduler(timezone='Asia/Taipei')
scheduler.add_job(push_daily_quote, 'cron', hour=12, minute=0)
scheduler.start()

@app.route('/')
def index():
    return '金句推播機器人執行中！'

# === 執行 Flask App ===
if __name__ == '__main__':
    push_daily_quote()  # 啟動時先測試推播一次（妳也可以拿掉這行）
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
