import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config
from bot.handlers import help_router, start_router, process_router


async def main():
    script_path = sys.argv[0]
    script_directory = os.path.dirname(os.path.abspath(script_path)) + '/logs.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(script_directory),  # Log to file
        ]
    )

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(process_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.cfg.BOT_TOKEN)
    asyncio.run(main())
