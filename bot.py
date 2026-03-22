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

# --- Lock-файл для одного процесса ---

LOCK_FILE = "/tmp/bot.lock"

def is_process_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except:
        return False

# --- Запуск бота с авто-восстановлением ---

async def start_bot():
    # --- LOCK ---
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = int(f.read())

            if is_process_alive(pid):
                print("Another live instance found, skipping polling")
                return
            else:
                print("Stale lock detected, overriding")
        except:
            print("Corrupted lock file, overriding")

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    # --- AUTO-RESTART LOOP ---
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
