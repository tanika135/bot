from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loader import bot
from main import dp


@dp.message_handler(commands=["history"], state=None)
async def history_handler(message: Message, state: FSMContext):
    """/history — вывод истории поиска отелей"""
    data = await state.get_data()
    history = data.get("history")
    if history:
        await message.answer("История поиска:")
        for command in history:
            await message.answer(f'Команда: {command["command"]} время: {command["time"]} '
                                 f'результат поиска: {command["hotels"]}')
    else:
        await message.answer("История поиска пустая!")
