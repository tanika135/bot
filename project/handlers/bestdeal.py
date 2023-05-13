from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from main import dp
from states.states import FSMHotels


@dp.message_handler(commands=["bestdeal"], state=None)
async def low_price_start(message: Message, state: FSMContext):
    """/bestdeal —  топ отелей, наиболее подходящих по цене и расположению от центра"""
    await FSMHotels.city.set()
    async with state.proxy() as data:
        data["sort"] = 'distance'
        data["bestdeal"] = 'y'
    await message.answer("В каком городе искать отель?")


@dp.message_handler(state=FSMHotels.min_price)
async def min_price(message: Message, state: FSMContext):
    try:
        answer = int(message.text)
        if answer >= 0:
            async with state.proxy() as data:
                data["min_price"] = answer
            await FSMHotels.max_price.set()
            await message.answer("Укажите максимальную цену за номер.")
        else:
            await message.answer("Минимальная цена не может быть меньше 0")
    except ValueError:
        await message.answer("Введите число")


@dp.message_handler(state=FSMHotels.max_price)
async def max_price(message: Message, state: FSMContext):
    try:
        answer = int(message.text)
        if answer > 0:
            async with state.proxy() as data:
                data["max_price"] = answer
            await FSMHotels.distance.set()
            await message.answer("Укажите расстояние до центра")
        else:
            await message.answer("Максимальная цена должна быть больше 0")
    except ValueError:
        await message.answer("Введите число")


@dp.message_handler(state=FSMHotels.distance)
async def distance(message: Message, state: FSMContext):
    try:
        answer = float(message.text)
        if answer > 0:
            async with state.proxy() as data:
                data["distance"] = answer
            await FSMHotels.num_results.set()
            await message.answer("Укажите количество отелей, которые необходимо вывести в результате (не более 5).")
        else:
            await message.answer("Расстояние до центра должно быть больше 0")
    except ValueError:
        await message.answer("Введите число")

