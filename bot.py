import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

@web.middleware
async def log_middleware(request, handler):
    print("REQUEST:", request.method, request.path)
    return await handler(request)

TOKEN = "8754421373:AAEoHSSZ8hOzaZ6gPORKLx4p0K5TyAWMoys"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ai-job-hunter-production-cc90.up.railway.app/webhook"

bot = Bot(token=TOKEN)
print("WEBHOOK URL:", WEBHOOK_URL)

dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я AI Job Hunter 🤖")

@dp.message()
async def echo(message: types.Message):
    await message.answer("Ты написал: " + message.text)

async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)

def main():
    app = web.Application(middlewares=[log_middleware])
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
