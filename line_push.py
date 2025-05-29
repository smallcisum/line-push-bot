import requests
import json
import random
import os
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import atexit # 為了在應用程式關閉時，讓排程器也能正常關閉

# === LINE 設定 ===
# 從環境變數讀取 LINE Bot 的 Channel Access Token
# 在部署平台（如 Heroku）上設定這個環境變數，例如：LINE_CHANNEL_ACCESS_TOKEN
CHANNEL_ACCESS_TOKEN = os.environ.get('e6e267f4ffc2be6d9e79e45cc15e0ab2')

# 從環境變數讀取 LINE 的 User ID，這是你想要推播的 LINE ID
# 在部署平台（如 Heroku）上設定這個環境變數，例如：LINE_USER_ID
USER_ID = os.environ.get('Ua1ee40b62de1333b9f167cb4cf5d33f7')

# 語錄來源，保持不變
BIBLE_JSON_URL = 'https://raw.githubusercontent.com/smallcisum/bible/main/bible.json'

app = Flask(__name__)

# 啟動時檢查必要的環境變數是否設定
if not CHANNEL_ACCESS_TOKEN:
    print("🚨 警告：LINE_CHANNEL_ACCESS_TOKEN 環境變數未設定！推播功能可能無法運作。")
if not USER_ID:
    print("🚨 警告：LINE_USER_ID 環境變數未設定！推播功能可能無法運作。")

# === 每日推播函數 ===
def push_daily_quote():
    # 如果缺少必要的 LINE 設定，則不執行推播
    if not CHANNEL_ACCESS_TOKEN or not USER_ID:
        print("🚨 推播失敗：LINE_CHANNEL_ACCESS_TOKEN 或 LINE_USER_ID 未設定，請檢查環境變數。")
        return

    try:
        # 嘗試從 GitHub 獲取金句
        res = requests.get(BIBLE_JSON_URL)
        # 檢查 HTTP 請求是否成功 (例如：狀態碼 200)
        res.raise_for_status() 
        quotes = json.loads(res.text)
        
        # 如果金句列表為空，則打印錯誤訊息
        if not quotes:
            print("🚨 錯誤：未從語錄來源獲取到任何金句，或金句列表為空。")
            return

        # 隨機選擇一句金句
        quote = random.choice(quotes)
        # 將金句格式化為字符串，如果是列表則用換行符連接
        text = '\n'.join(quote) if isinstance(quote, list) else str(quote)

        # 設定 LINE Push Message API 的標頭
        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        # 設定 LINE Push Message API 的請求體
        body = {
            "to": USER_ID,
            "messages": [{
                "type": "text",
                "text": f"📖 今日金句：\n{text}"
            }]
        }

        # 發送推播訊息到 LINE
        r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(body))
        # 檢查 LINE API 的回應是否成功
        r.raise_for_status() 
        
        # 打印調試信息
        print("LINE 回應狀態碼：", r.status_code)
        print("LINE 回應內容：", r.text)
        print("✅ 推播成功" if r.status_code == 200 else "⚠️ 推播失敗")

    except requests.exceptions.RequestException as req_err:
        print(f"🚨 網路請求或 LINE API 錯誤：{req_err}")
    except json.JSONDecodeError as json_err:
        print(f"🚨 JSON 解析錯誤，金句來源格式可能不正確：{json_err}")
    except Exception as e:
        print(f"🚨 發生未預期錯誤：{e}")

# === 每日定時排程（中午 12:00 台北時間）===
# 使用 BackgroundScheduler 在後台運行排程任務
scheduler = BackgroundScheduler(timezone='Asia/Taipei')
# 設定每天中午 12 點 0 分 0 秒觸發 push_daily_quote 函數
scheduler.add_job(push_daily_quote, 'cron', hour=12, minute=0, second=0)
scheduler.start()

# 確保在應用程式關閉時，排程器也能正常關閉
atexit.register(lambda: scheduler.shutdown())

# === 網頁路由 ===
# 根路由，訪問網站時顯示的訊息
@app.route('/')
def index():
    return '💌 金句推播機器人執行中！'

# 手動發送金句的路由，可以用於測試
@app.route('/send')
def manual_send():
    push_daily_quote()
    # 返回 JSON 格式的狀態訊息，方便檢查
    return jsonify({"status": "success", "message": "📨 金句發送請求已送出！請檢查伺服器日誌確認推播結果。"})

# === 執行 Flask App ===
if __name__ == '__main__':
    # 從環境變數中獲取端口號，如果沒有則使用 5000
    # 部署平台會設定一個 PORT 環境變數
    port = int(os.environ.get("PORT", 5000))
    # 讓 Flask 應用程式在所有可用的 IP 地址上監聽
    app.run(host="0.0.0.0", port=port)
