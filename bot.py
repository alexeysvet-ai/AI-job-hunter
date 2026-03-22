import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = "8754421373:AAGnnit9_UG7hUWVgagSiAe3galq8INWbJ0"
BASE_URL = "https://ai-job-hunter-69q8.onrender.com"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Handlers ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я AI Job Hunter 🤖")

@dp.message()
async def echo(message: types.Message):
    text = message.text or "не текстовое сообщение"
    await message.answer("Ты написал: " + text)

# --- Startup / Shutdown ---

async def on_startup(app):
    print("Setting webhook:", WEBHOOK_URL)
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    print("Deleting webhook")
    await bot.delete_webhook()

# --- Main app ---

def create_app():
    app = web.Application()

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # health check
    async def health(request):
        return web.Response(text="OK")

    app.router.add_get("/", health)

    return app

# --- Run ---

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app = create_app()
    print(f"Starting webhook server on port {port}")
    web.run_app(app, host="0.0.0.0", port=port)
