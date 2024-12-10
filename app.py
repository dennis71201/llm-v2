from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import requests
import json

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

# 定義 API 的 URL 和 Bearer Token
api_url = "https://4f7c-59-125-76-248.ngrok-free.app/api/v1/workspace/0822/chat"
bearer_token = "Z824BPY-18PMX2R-KPW1A14-X8DDYBJ"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 準備要傳送的資料
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    data = {
        "message": event.message.text,
        "mode": "query"
    }
    
    try:
        # 發送 POST 請求
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # 檢查是否有請求錯誤
        response_data = response.json()
        # 取得 textResponse 並作為回應
        text_response = response_data.get('textResponse', "無法取得回應。")
        message = TextSendMessage(text=text_response)
    except requests.exceptions.RequestException as e:
        # 如果請求發生錯誤，回傳錯誤訊息
        message = TextSendMessage(text=f"無法處理請求: {str(e)}")
    except KeyError:
        # 如果無法取得 textResponse，回傳預設錯誤訊息
        message = TextSendMessage(text="回應格式錯誤，無法取得回應。")
    
    # 回應使用者
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
