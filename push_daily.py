import requests
import json
import random

CHANNEL_ACCESS_TOKEN = 'NFutE++FSNU/qXNjdTz9eaAnfBGQSLMDD+W/DFg7LuCiIvzc9i0IxgMahJigyF9gzPfKdTHcQJfrDh2glPLJeiOeOOsD6tEV9GwKGscFaolDao1pmiuZVSf+nWhKJsoqLLxMjK1KxXWfenBqbyGKEAdB04t89/1O/w1cDnyilFU='
USER_ID = 'Ua1ee40b62de1333b9f167cb4cf5d33f7'
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

        body = {
            "to": USER_ID,
            "messages": [{
                "type": "text",
                "text": f"📖 今日金句：\n{text}"
            }]
        }

        r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(body))
        print("✅ 推播成功" if r.status_code == 200 else f"⚠️ 推播失敗：{r.text}")

    except Exception as e:
        print("🚨 發生錯誤：", e)

push_daily_quote()
