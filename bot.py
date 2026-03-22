import os
import asyncio
import socket
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8754421373:AAEEvOvnyV1GFOPd4YaQINc-PfvwlWfHPT8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Telegram handlers ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я AI Job Hunter 🤖")

@dp.message()
async def echo(message: types.Message):
    text = message.text or "не текстовое сообщение"
    await message.answer("Ты написал: " + text)

# --- Определяем главный процесс ---

def is_main_process():
    hostname = socket.gethostname()
    print("HOSTNAME:", hostname)
    return hostname.endswith("0")

# --- Запуск бота ---

async def start_bot():

    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot started...")
    await dp.start_polling(bot)

# --- HTTP сервер для Render ---

async def handle(request):
    return web.Response(text="OK")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))
    print("Starting web server on port:", port)
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- Main ---

async def main():
    await asyncio.gather(
        start_bot(),
        start_web()
    )

if __name__ == "__main__":
    asyncio.run(main())
