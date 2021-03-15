from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('WASdhw2WvNUGyxS43/+oINY6UAxlXbVZJMcGC5HkDJR8Q0kZT7kQRHNe/j7JVJoy3ENbl27AZXEe+GFS2dDPM5P4GZ5HmUg1eLrwZps9YbJOE0LD+l5YlvcUTDc2TrHBKscbaWA20/rgAIdZ+6EjXQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('669c563f1bd4d59642a707326935e4ea')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
