from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database.storage import DB
from loader import bot
from main import dp


@dp.message_handler(commands=["history"], state=None)
async def history_handler(message: Message, state: FSMContext):
    """/history — вывод истории поиска отелей"""
    db = DB()
    history = db.read_history(chat_id=message.chat.id, limit=5)

    if history:
        await message.answer("История поиска:")
        for command in history:
            hotels = ''
            for hotel in command[4]:
                hotels += hotel[2]
            await message.answer(f'Команда: {command[2]} время: {command[3]} '
                                 f'резльтат поиска: {hotels}')
    else:
        await message.answer("История поиска пустая!")
