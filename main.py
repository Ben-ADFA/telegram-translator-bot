import os
import asyncio
from aiogram import Bot, Dispatcher, types
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def translate(message: types.Message):
    if not message.text:
        return

    try:
        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(message.text)

        await message.answer(f"🌐 {translated}")
    except Exception as e:
        await message.answer(f"Error: {e}")

async def main():
    print("Bot running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
