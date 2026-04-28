import os
import random
import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- НАСТРОЙКИ ---
TOKEN = '8693879510:AAHqWuXS-MiiTWexzPt9FD0VUBRjb3R0dgY'
CHAT_ID =  823414394  # ID парня
PHOTO_DIR = './photoes/'  # На Render путь будет проще

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

async def send_daily_photo():
    try:
        all_photos = os.listdir(PHOTO_DIR)
        if not all_photos:
            return
        random_photo = random.choice(all_photos)
        photo_path = os.path.join(PHOTO_DIR, random_photo)
        photo = FSInputFile(photo_path)
        await bot.send_photo(CHAT_ID, photo, caption="Лови наше воспоминание! ❤️")
    except Exception as e:
        print(f"Ошибка: {e}")

async def main():
    scheduler.add_job(send_daily_photo, 'cron', hour=10, minute=0)
    scheduler.start()
    await send_daily_photo() # Сразу отправим одно для проверки
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())