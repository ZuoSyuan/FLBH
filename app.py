import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage,
    QuickReply,
    QuickReplyButton,
)
from linebot.models import (
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
)

from TextConstant import *
from FlexMessageJson import *

app = Flask(__name__)

on_heroku = True
if on_heroku:
    line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
    handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
else:
    app.run(debug=True)
    from secret import *
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

def make_reply(text):
    msg = ''
    if text == FLEX_MESSAGE_DEMO:
        msg = FLEX_MESSAGE_DEMO
    elif text == QUICK_REPLY_DEMO:
        msg = QUICK_REPLY_DEMO
    elif text == GET_MESSAGE_DELIVERY_REPLY:
        resp = line_bot_api.get_message_delivery_reply(date='20211104')
        msg = f'Total [{resp.success}] reply messages sent.'
    else:
        msg = "Echo => " + text
    return msg

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    
    msg = make_reply(get_message)
    
    if msg == FLEX_MESSAGE_DEMO:
        flex_message = FlexSendMessage(
            alt_text='PowerDVD',
            contents=POWERDVD_FLEX_MESSAGE_JSOM
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif msg == QUICK_REPLY_DEMO:
        message=TextSendMessage(
            text="文字訊息",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(label="Postback",data="回傳資料")
                        ),
                    QuickReplyButton(
                        action=MessageAction(label="文字訊息",text="回傳文字")
                        ),
                    QuickReplyButton(
                        action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime')
                        ),
                    QuickReplyButton(
                        action=CameraAction(label="拍照")
                        ),
                    QuickReplyButton(
                        action=CameraRollAction(label="相簿")
                        ),
                    QuickReplyButton(
                        action=LocationAction(label="傳送位置")
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    else:
        # Send To Line
        reply = TextSendMessage(text=f"{msg}")
        line_bot_api.reply_message(event.reply_token, reply)


