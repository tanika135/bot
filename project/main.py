import asyncio
from aiogram import Bot, Dispatcher, executor
from loader import bot

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

else:
    loop = asyncio.get_event_loop()

dp = Dispatcher(bot, loop=loop)

if __name__ == '__main__':
    from handlers.help import dp
    print('running')
    executor.start_polling(dp)

