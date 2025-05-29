import os
import requests
import json
from flask import Flask
from datetime import datetime
import pytz

app = Flask(__name__)

# ==== LINE Bot 設定 ====
CHANNEL_ACCESS_TOKEN = "你的 Channel access token"  # ⚠️請填入自己的
USER_ID = "Ua1ee40b62de1333b9f167cb4cf5d33f7"       # 小公主妳的 userId ✅

# ==== 金句 JSON 來源 ====
QUOTES_URL = "https://raw.githubusercontent.com/smallcisum/bible/main/bible.json"

def load_quotes():
    try:
        res = requests.get(QUOTES_URL, timeout=5)
        data = res.json()
        return data
    except Exception as e:
        print("❌ 讀取金句失敗：", e)
        return []

def get_today_quote():
    quotes = load_quotes()
    if not quotes:
        return "今天沒有金句 😢"
    index = datetime.now(pytz.timezone("Asia/Taipei")).day % len(quotes)
    q = quotes[index]
    # 支援 2~3 欄位的 tuple
    if isinstance(q, list) and len(q) == 3:
        return f"{q[0]}\n{q[1]}\n📖 {q[2]}"
    elif isinstance(q, list) and len(q) == 2:
        return f"{q[0]}\n{q[1]}"
    else:
        return str(q)

def push_daily_quote():
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    message = {
        "to": USER_ID,
        "messages": [{
            "type": "text",
            "text": get_today_quote()
        }]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push",
                             headers=headers, data=json.dumps(message))
    if response.status_code == 200:
        print("✅ 推播成功")
    else:
        print(f"⚠️ 推播失敗：{response.status_code} {response.text}")

# === Flask Routes ===
@app.route('/')
def index():
    return '📖 金句機器人運行中！'

@app.route('/send')
def send_quote_now():
    push_daily_quote()
    return '📨 已發送一次金句給你！'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
