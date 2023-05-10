from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from main import dp
from states.states import FSMHotels


@dp.message_handler(commands=["highprice"], state=None)
async def low_price_start(message: Message, state: FSMContext):
    """/highprice — вывод самых дешёвых отелей в городе,"""
    await FSMHotels.city.set()
    async with state.proxy() as data:
        data["sort"] = 'h2l'
    await message.answer("В каком городе искать отель?")
