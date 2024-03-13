import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

lineTokenFile = open('LineToken.json', 'r')
lineTokenData = json.load(lineTokenFile)

line_bot_api = LineBotApi(lineTokenData['LineAccessToken'])
handler = WebhookHandler(lineTokenData['LineChannelSecret'])


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    userMsg = event.message.text

    if userMsg == '你好':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='我一點都不好'))
    elif userMsg == '你是誰':
        sticker_message = StickerSendMessage(
            package_id='446',
            sticker_id='1991'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)