import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("8754421373:AAFsF9rFolRlWXcNvo1Koahal1CaoMhK420")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я AI Job Hunter 🤖")

@dp.message()
async def echo(message: types.Message):
    await message.answer("Ты написал: " + message.text)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
