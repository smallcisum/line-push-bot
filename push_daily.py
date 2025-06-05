import requests
import json
import random

# === LINE 設定 ===
CHANNEL_ACCESS_TOKEN = 'NFutE++FSNU/qXNjdTz9eaAnfBGQSLMDD+W/DFg7LuCiIvzc9i0IxgMahJigyF9gzPfKdTHcQJfrDh2glPLJeiOeOOsD6tEV9GwKGscFaolDao1pmiuZVSf+nWhKJsoqLLxMjK1KxXWfenBqbyGKEAdB04t89/1O/w1cDnyilFU='

# ✅ 多人推播：把使用者 ID 放這裡
USER_IDS = [
    'Ua1ee40b62de1333b9f167cb4cf5d33f7',  # 我
    'U5541c4ea444409050ad321ae7d0db489'          # ← 昱翰ID
]

# === 金句資料來源 ===
BIBLE_JSON_URL = 'https://raw.githubusercontent.com/smallcisum/bible/main/bible.json'

def push_daily_quote():
    try:
        res = requests.get(BIBLE_JSON_URL)
        quotes = json.loads(res.text)
        quote = random.choice(quotes)

        text = (
            f"{quote.get('zh', '')}\n"
            f"{quote.get('en', '')}\n\n"
            f"📍 {quote.get('zh_ref', '')} | {quote.get('en_ref', '')}\n"
            f"🔖 主題：{quote.get('topic', '')}"
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
                    "text": f"📖 今日金句：\n{text}"
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
