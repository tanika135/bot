from requests import get

from config_data import config
import requests
import telebot
from dotenv import load_dotenv
import os


def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    # В зависимости от типа запроса вызываем соответствующую функцию
    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    # else:
    #     return post_request(
    #         url=url,
    #         params=params
    #     )


def get_request(url, params):
    try:
        response = get(
            url,
            #headers=...,
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.json()
    except ValueError as error:
        print('Ошибка приложения: ' + str(error))


class TelegramBot:
    def __init__(self):

        self.__bot_token = config.BOT_TOKEN
        self.__city = ''

    def run(self):




        @bot.message_handler(commands=['lowprice'])
        def lowprice_handler(message):
            """/lowprice — вывод самых дешёвых отелей в городе"""
            bot.reply_to(message, "В каком городе искать отель?")
            print('1')


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


