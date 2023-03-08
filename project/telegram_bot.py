import requests
import telebot
from dotenv import load_dotenv
import os


class TelegramBot:
    def __init__(self):
        load_dotenv()
        self.__api_token = os.environ['API_TOKEN']

    def run(self):
        bot = telebot.TeleBot(self.__api_token)
        print('running')

        @bot.message_handler(commands=['help'])
        def help_handler(message):
            """/help — помощь по командам бота,"""
            bot.reply_to(message, """
/help — помощь по командам бота,
/lowprice — вывод самых дешёвых отелей в городе,
/highprice — вывод самых дорогих отелей в городе,
/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра.
/history — вывод истории поиска отелей.
            """)

        @bot.message_handler(commands=['lowprice'])
        def lowprice_handler(message):
            """/lowprice — вывод самых дешёвых отелей в городе"""
            bot.reply_to(message, " command - lowprice")

        @bot.message_handler(commands=['highprice'])
        def highprice_handler(message):
            """/highprice — вывод самых дорогих отелей в городе,"""
            bot.reply_to(message, " command - highprice")

        @bot.message_handler(commands=['bestdeal'])
        def bestdeal_handler(message):
            """/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра"""
            bot.reply_to(message, " command - bestdeal")

        @bot.message_handler(commands=['history'])
        def history_handler(message):
            """/history — вывод истории поиска отелей"""
            bot.reply_to(message, " command - history")

        @bot.message_handler(func=lambda message: True)
        def echo_message(message):
            if message.text.lower() == "привет" or message.text == "/hello_world":
                bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
            else:
                bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

        bot.infinity_polling()


