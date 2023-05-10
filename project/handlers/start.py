from aiogram.types import Message
from main import dp
from aiogram.dispatcher import filters
from loader import bot

HI = [
    'Привет',
    'привет'
]


@dp.message_handler(commands=["start"])
async def hello_world(message: Message):
    await message.reply(f"Для начала работы напиши /help.")


@dp.message_handler(commands=["hello_world"])
@dp.message_handler(filters.Text(contains=HI, ignore_case=True))
async def hello_world(message: Message):
    await message.reply(f"Привет, {message.from_user.full_name}!")

