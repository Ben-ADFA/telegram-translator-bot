import os
import time
import requests
import langid
from deep_translator import MyMemoryTranslator
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

offset = 0

# Map langid's 2-letter codes to the locale codes MyMemory expects
LANG_CODE_MAP = {
    "es": "es-ES", "fr": "fr-FR", "de": "de-DE", "it": "it-IT",
    "pt": "pt-PT", "nl": "nl-NL", "ru": "ru-RU", "zh": "zh-CN",
    "ja": "ja-JP", "ko": "ko-KR", "ar": "ar-SA",
    "hi": "hi-IN", "tr": "tr-TR", "pl": "pl-PL", "sv": "sv-SE",
    "uk": "uk-UA", "vi": "vi-VN", "th": "th-TH", "id": "id-ID",
}


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
    print("🚀 BOT LOOP STARTED")
    while True:
        updates = get_updates()
        if updates:
            print("Updates received:", len(updates))
        for update in updates:
            print("RAW UPDATE:", update)
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            text = message.get("text")
            chat_id = message["chat"]["id"]
            if not text:
                continue

            print("TEXT:", text)

            detected, confidence = langid.classify(text)
            print("DETECTED LANG:", detected, "CONFIDENCE:", confidence)

            if detected == "en":
                continue

            source_code = LANG_CODE_MAP.get(detected)
            if not source_code:
                print(f"No mapping for '{detected}', skipping")
                continue

            try:
                translated = MyMemoryTranslator(
                    source=source_code,
                    target="en-US"
                ).translate(text)

                if translated.strip().lower() == text.strip().lower():
                    continue

                send_message(chat_id, f"🌐 {translated}")
            except Exception as e:
                print("Translation error:", e)

        time.sleep(1)


if __name__ == "__main__":
    bot_loop()