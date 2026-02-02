import os
from flask import Flask, request, jsonify, render_template,abort
from dotenv import load_dotenv
from google import genai
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY2")
if not API_KEY:
    raise RuntimeError("找不到 GEMINI_API_KEY2，請在 .env 設定：GEMINI_API_KEY2=你的Key")

client = genai.Client(api_key=API_KEY)

# Line Bot 相關設定（若未設定則設為 None，避免啟動失敗）
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

if CHANNEL_ACCESS_TOKEN:
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
else:
    line_bot_api = None
    
if CHANNEL_SECRET:
    handler = WebhookHandler(CHANNEL_SECRET)
else:
    handler = None


# 你可換成你帳號可用的模型
MODEL = "gemini-2.5-flash"

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=message,
        )
        reply = getattr(resp, "text", None) or ""
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/callback", methods=['POST'])
def callback():
    if not handler:
        return 'Line Bot handler not configured', 400
        
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def handle_message(event):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=event.message.text
    )

    message = TextSendMessage(text=response.text)
    line_bot_api.reply_message(event.reply_token, message)


if handler:
    handler.add(MessageEvent, message=TextMessage)(handle_message)


if __name__ == "__main__":
    # mac 常見 5000 被占用，改 5050 比較省事
    app.run(host="127.0.0.1", port=5050, debug=True)
