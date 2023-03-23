from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["lowprice"])
def bot_low_price(message: Message):
    """/lowprice — вывод самых дешёвых отелей в городе,"""
    bot.reply_to(message, "В каком городе искать отель?")
