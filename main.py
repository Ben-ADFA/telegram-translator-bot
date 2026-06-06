import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    translated = GoogleTranslator(source="auto", target="en").translate(text)

    await update.message.reply_text(f"🌐 {translated}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()