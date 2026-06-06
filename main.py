import os
import time
import threading
import requests
from flask import Flask
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

offset = 0

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def get_updates():
    global offset
    try:
        r = requests.get(
            f"{BASE_URL}/getUpdates",
            params={"offset": offset, "timeout": 10}
        )
        return r.json().get("result", [])
    except Exception as e:
        print("get_updates error:", e)
        return []

def send_message(chat_id, text):
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            data={"chat_id": chat_id, "text": text}
        )
    except Exception as e:
        print("send_message error:", e)

def bot_loop():
    global offset

    print("Bot started...")

    while True:
        updates = get_updates()

        for update in updates:
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message or "text" not in message:
                continue

            text = message["text"]
            chat_id = message["chat"]["id"]

            try:
                translated = GoogleTranslator(
                    source="auto",
                    target="en"
                ).translate(text)

                send_message(chat_id, f"🌐 {translated}")

            except Exception as e:
                send_message(chat_id, f"Error: {e}")

        time.sleep(1)

# Start bot in background
threading.Thread(target=bot_loop, daemon=True).start()

# Start web server (THIS is what Render needs)
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
