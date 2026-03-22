import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8754421373:AAEEvOvnyV1GFOPd4YaQINc-PfvwlWfHPT8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я AI Job Hunter 🤖")

@dp.message()
async def echo(message: types.Message):
    await message.answer("Ты написал: " + message.text)

async def main():
    # на всякий случай сбрасываем webhook
    await bot.delete_webhook(drop_pending_updates=True)

    print("Bot started...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
