import os
import requests
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

offset = 0

def get_updates():
    global offset
    r = requests.get(f"{URL}/getUpdates", params={"offset": offset}).json()
    return r.get("result", [])

def send_message(chat_id, text):
    requests.post(f"{URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

print("Bot running...")

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
            translated = GoogleTranslator(source="auto", target="en").translate(text)
            send_message(chat_id, f"🌐 {translated}")
        except Exception as e:
            send_message(chat_id, f"Error: {e}")
