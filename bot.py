import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8754421373:AAGnnit9_UG7hUWVgagSiAe3galq8INWbJ0"
BASE_URL = "https://ai-job-hunter-69q8.onrender.com"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- handlers ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я AI Job Hunter 🤖")

@dp.message()
async def echo(message: types.Message):
    text = message.text or "не текстовое сообщение"
    await message.answer("Ты написал: " + text)

# --- webhook handler ---

async def handle_webhook(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# --- startup ---

async def on_startup(app):
    print("Setting webhook:", WEBHOOK_URL)
    await bot.set_webhook(WEBHOOK_URL)

# --- health ---

async def health(request):
    return web.Response(text="OK")

# --- main ---

def create_app():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.router.add_get("/", health)
    app.on_startup.append(on_startup)
    return app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app = create_app()
    print(f"Starting server on port {port}")
    web.run_app(app, host="0.0.0.0", port=port)
