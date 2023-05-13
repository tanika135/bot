from aiogram.types import Message
from main import dp
from aiogram.dispatcher import FSMContext
from states.states import FSMHotels
from utils.hotel_api import api_request, search_locations, start_search


@dp.message_handler(commands=["lowprice"], state=None)
async def low_price_start(message: Message, state: FSMContext):
    """/lowprice — вывод самых дешёвых отелей в городе,"""
    await FSMHotels.city.set()
    async with state.proxy() as data:
        data["sort"] = 'l2h'
    await message.answer("В каком городе искать отель?")


@dp.message_handler(state=FSMHotels.city)
async def enter_city_name(message: Message, state: FSMContext):
    city = message.text

    result = search_locations(city)
    async with state.proxy() as data:
        data["city_results"] = result
        if len(result) > 0:
            data["city_gues"] = 0

    if len(result) > 0:
        await message.answer(f'В ищите отели в: {result[0]["name"]} ?')
        await FSMHotels.city_confirm.set()
    else:
        await message.answer("По вашему запросу ничего не найдено. Попробуйте другой город.")


@dp.message_handler(state=FSMHotels.city_confirm)
async def confirm_city(message: Message, state: FSMContext):
    confirm = message.text.lower() == "да"

    data = await state.get_data()
    city_gues = data.get("city_gues")
    result = data["city_results"]
    if confirm:
        async with state.proxy() as data:
            data["city_confirm"] = city_gues
        await FSMHotels.num_results.set()
        await message.answer(f'Ищем отели в: {result[city_gues]["name"]}')
        await message.answer("Укажите количество отелей, которые необходимо вывести в результате (не более 5).")
    else:
        async with state.proxy() as data:
            next_city = city_gues + 1
            if next_city < len(result):
                data["city_gues"] = next_city
                await message.answer(f'В ищите отели в: {result[next_city]["name"]} ?')
            else:
                await FSMHotels.city.set()
                await message.answer("По вашему запросу ничего не найдено. Попробуйте другой город.")


@dp.message_handler(state=FSMHotels.num_results)
async def num_hotels(message: Message, state: FSMContext):
    try:
        answer = int(message.text)
        if 0 < answer < 6:
            async with state.proxy() as data:
                data["num_res"] = answer
            await FSMHotels.need_photo.set()
            await message.answer("Необходимо ли вывести фотографии для каждого отеля? Да/Нет")

        else:
            await message.answer("Введите число от 1 до 5")
    except ValueError:
        await message.answer("Введите число от 1 до 5")


@dp.message_handler(state=FSMHotels.need_photo)
async def need_photo(message: Message, state: FSMContext):
    need_photo = message.text.lower()
    if need_photo in ("да", "нет"):

        if need_photo == "да":
            await FSMHotels.num_photo.set()
            await message.answer("Введите число от 1 до 3")
        else:
            await start_search(message, state, False)
    else:
        await message.answer("Введите Да или Нет")


@dp.message_handler(state=FSMHotels.num_photo)
async def num_photo(message: Message, state: FSMContext):
    try:
        answer = int(message.text)
        if 0 < answer < 4:
            async with state.proxy() as data:
                data["num_photo"] = answer
            await start_search(message, state, True)
        else:
            await message.answer("Введите число от 1 до 3")
    except ValueError:
        await message.answer("Введите число от 1 до 3")


