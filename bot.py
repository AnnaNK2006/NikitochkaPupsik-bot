import os
import random
import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web # Добавили это

TOKEN = 'ТВОЙ_ТОКЕН_ТУТ'
CHAT_ID = ТВОЙ_ID_ТУТ
PHOTO_DIR = os.path.join(os.path.dirname(__file__), 'photos')

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

async def send_daily_photo():
    try:
        all_photos = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not all_photos:
            print("В папке нет фото!")
            return
        random_photo = random.choice(all_photos)
        photo_path = os.path.join(PHOTO_DIR, random_photo)
        photo = FSInputFile(photo_path)
        await bot.send_photo(CHAT_ID, photo, caption="Лови наше воспоминание! ❤️")
        print("Фото успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")

# Это «заглушка» для Render, чтобы он думал, что это сайт
async def handle(request):
    return web.Response(text="Bot is alive!")

async def main():
    # Настройка мини-сайта
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', os.getenv('PORT', 10000))
    
    # Запуск сайта и планировщика
    asyncio.create_task(site.start())
    
    scheduler.add_job(send_daily_photo, 'cron', hour=10, minute=0)
    scheduler.start()
    
    await send_daily_photo() # Пробная отправка
    
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
