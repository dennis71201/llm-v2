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

# url = "http://192.168.0.231:3001/api/v1/workspace/kebbi-demo/chat"#注意t1的值，每個人的不一樣
# api_key = "855077P-2YW420X-JDS7907-DATXR78"#自訂，每個人的不一樣

# headers = {
#     "accept": "application/json",
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

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
    # data = {
    # "message": event.message.text,
    # "mode": "query"
    # }
    # response = requests.post(url, headers=headers, data=json.dumps(data))
    # print(response.json()['textResponse'])
    if event.message.text=="台大雲林分院內外科綜合加護病房的訪客時間是什麼時候":
        message = TextSendMessage('訪客時間為一天一次，時間為10點半到11點。')
    elif event.massage.text=="骨髓穿刺檢查需要多少時間":
        message = TextSendMessage('骨髓穿刺檢查整個過程約20至30分鐘。')
    elif event.massage.text=="放射線皮膚炎多發生於治療後的哪一個時間段":
        message = TextSendMessage('放射線皮膚炎的主要發生時期為治療後兩道三週內，特別是在照射部位為頭頸部、胸部及臀部時。')
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    






