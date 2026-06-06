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

def is_english(text):
    return all(ord(c) < 128 for c in text)

def bot_loop():
    global offset

    print("🚀 BOT LOOP STARTED")  # IMPORTANT DEBUG

    while True:
        updates = get_updates()

        if updates:
            print("Updates:", len(updates))

        for update in updates:
            print("RAW:", update)

            offset = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            text = message.get("text")
            chat_id = message["chat"]["id"]

            print("TEXT:", text)

            try:
                if is_english(text):
                    continue

                translated = GoogleTranslator(
                    source="auto",
                    target="en"
                ).translate(text)

                send_message(chat_id, f"🌐 {translated}")

            except Exception as e:
                print("Translation error:", e)

        time.sleep(1)

def start_bot():
    print("Starting bot thread...")
    bot_loop()

if __name__ == "__main__":
    # Start bot FIRST in background
    threading.Thread(target=start_bot, daemon=True).start()

    # Then start Flask
    port = int(os.environ.get("PORT", 10000))
    print("Starting Flask...")
    app.run(host="0.0.0.0", port=port)
