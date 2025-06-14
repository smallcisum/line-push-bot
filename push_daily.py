from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import json
import random

# === LINE 設定 ===
CHANNEL_ACCESS_TOKEN = 'NFutE++FSNU/qXNjdTz9eaAnfBGQSLMDD+W/DFg7LuCiIvzc9i0IxgMahJigyF9gzPfKdTHcQJfrDh2glPLJeiOeOOsD6tEV9GwKGscFaolDao1pmiuZVSf+nWhKJsoqLLxMjK1KxXWfenBqbyGKEAdB04t89/1O/w1cDnyilFU='

# ✅ 多人推播：把使用者 ID 放這裡
USER_IDS = [
    'Ua1ee40b62de1333b9f167cb4cf5d33f7',  # 我
    'U5541c4ea444409050ad321ae7d0db489'  # 昱翰
]

# === 金句資料來源 ===
BIBLE_JSON_URL = 'https://raw.githubusercontent.com/smallcisum/bible/main/bible.json'

def push_daily_quote():
    try:
        # 台北時區（ZoneInfo）
        now = datetime.now(ZoneInfo("Asia/Taipei"))
        weekday_map = ["一", "二", "三", "四", "五", "六", "日"]
        weekday = weekday_map[now.weekday()]
        date_str = f" {now.strftime('%Y-%m-%d')}（{weekday}） 金句"

        # 取得金句與祝福與結語
        res = requests.get(BIBLE_JSON_URL)
        data = json.loads(res.text)

        quotes = data["verses"]
        blessings = data["blessings"]
        closing_lines = data["closing_lines"]

        quote = random.choice(quotes)
        blessing = random.choice(blessings)
        closing = random.choice(closing_lines)

        # 組合訊息文字
        text = (
            f"{date_str}\n\n"
            f"{quote.get('zh', '')}\n"
            f"{quote.get('en', '')}\n\n"
            f"📍 {quote.get('zh_ref', '')} | {quote.get('en_ref', '')}\n"
            f"🔖 主題：{quote.get('topic', '')}\n\n"
            f"💌 {blessing}\n\n"
            f"{closing}"
        )

        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        for user_id in USER_IDS:
            body = {
                "to": user_id,
                "messages": [{
                    "type": "text",
                    "text": text
                }]
            }

            r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(body))
            if r.status_code == 200:
                print(f"✅ 成功推播給 {user_id}")
            else:
                print(f"⚠️ 推播失敗 ({user_id})：{r.text}")

    except Exception as e:
        print("🚨 發生錯誤：", e)

# === 執行 ===
push_daily_quote()
