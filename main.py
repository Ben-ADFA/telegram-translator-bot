import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    try:
        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(update.message.text)

        await update.message.reply_text(f"🌐 {translated}")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    if not TOKEN:
        print("BOT_TOKEN missing")
        return

    print("Bot running...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, translate)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
