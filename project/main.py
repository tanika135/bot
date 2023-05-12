import asyncio
from aiogram import Bot, Dispatcher, executor
from loader import bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

else:
    loop = asyncio.get_event_loop()

dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def on_startup(_):
    print('running')

if __name__ == '__main__':
    from handlers.help import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

