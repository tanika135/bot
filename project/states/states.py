from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMHotels(StatesGroup):
    city = State()
    city_confirm = State()
    num_results = State()
    need_photo = State()
    num_photo = State()
