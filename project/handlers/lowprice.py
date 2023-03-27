from aiogram.types import Message
from loader import bot

from utils.hotel_api import api_request
import json


# @bot.message_handler(commands=["lowprice"], state=None)
# def bot_low_price(message: Message):
#     """/lowprice — вывод самых дешёвых отелей в городе,"""
#     params = {'q': 'Рига', 'locale': 'ru_RU'}
#     #res = api_request(method_endswith='locations/v3/search', params=params, method_type='GET')
#     print(res)
#     bot.reply_to(message, "В каком городе искать отель?")
