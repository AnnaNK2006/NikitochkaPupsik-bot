import os
import random
import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

# --- ДАННЫЕ (заполни свои) ---
TOKEN = '8693879510:AAHqWuXS-MiiTWexzPt9FD0VUBRjb3R0dgY'
CHAT_ID =  823414394
PHOTO_DIR = os.path.join(os.path.dirname(__file__), 'photoes')

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

async def send_daily_photo():
    try:
        if not os.path.exists(PHOTO_DIR):
            print(f"Ошибка: Папка {PHOTO_DIR} не найдена!")
            return
        
        all_photos = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not all_photos:
            print("В папке нет подходящих фото!")
            return
            
        random_photo = random.choice(all_photos)
        photo_path = os.path.join(PHOTO_DIR, random_photo)
        photo = FSInputFile(photo_path)
        
        await bot.send_photo(CHAT_ID, photo, caption="Лови наше воспоминание! ❤️")
        print(f"Успех! Отправлено фото: {random_photo}")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")

# Код для "обмана" Render (чтобы он думал, что это сайт)
async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    # 1. Запуск мини-сервера для порта
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render передает порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Сервер запущен на порту {port}")

    # 2. Настройка планировщика (каждый день в 10:00)
    scheduler.add_job(send_daily_photo, 'cron', hour=10, minute=0, timezone='Asia/Almaty')
    scheduler.start()

    # 3. Мгновенная проверка при запуске
    await send_daily_photo()

    # Бесконечный цикл, чтобы бот не выключался
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())
