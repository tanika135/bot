import asyncio
from aiogram import Bot, Dispatcher, executor
from loader import bot


loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop)

if __name__ == '__main__':
    from handlers.help import start_bot, dp
    print('running')
    executor.start_polling(dp, on_startup=start_bot)

