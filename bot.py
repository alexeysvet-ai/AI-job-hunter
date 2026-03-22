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

# --- Atomic lock (без race condition) ---

LOCK_FILE = "/tmp/bot.lock"

def acquire_lock():
    try:
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w") as f:
            f.write(str(os.getpid()))
        return True
    except OSError as e:
        if e.errno == errno.EEXIST:
            print("Lock already exists, skipping polling")
            return False
        raise

# --- Bot runner (с авто-восстановлением) ---

async def start_bot():
    if not acquire_lock():
        return

    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            print("Bot started...")
            await dp.start_polling(bot)

        except Exception as e:
            print("Bot crashed:", e)
            print("Restarting in 5 seconds...")
            await asyncio.sleep(5)

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
