from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from handlers import reg_handlers

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

reg_handlers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())