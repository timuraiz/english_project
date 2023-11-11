import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config.config import config
from src.bot.handlers import help_router, start_router, process_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(process_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.BOT_TOKEN)
    asyncio.run(main())