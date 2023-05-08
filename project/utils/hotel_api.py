from requests import get, post
import requests
from config_data import config
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import datetime
from loader import bot
import json


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
    else:
        return post_request(
            url=url,
            params=params
        )


def get_request(url, params):
    try:
        response = get(
            url,
            headers={
                "X-RapidAPI-Key": config.RAPID_API_KEY,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            },
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.json()
    except ValueError as error:
        print('Ошибка приложения: ' + str(error))


def post_request(url, params):
    try:
        response = post(
            url,
            headers={
                "content-type": "application/json",
                "X-RapidAPI-Key": config.RAPID_API_KEY,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            },
            json=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.json()
    except ValueError as error:
        print('Ошибка приложения: ' + str(error))

async def start_search(message: Message, state: FSMContext, need_photo):

    data = await state.get_data()
    num_res = data.get("num_res")
    city_gues = data.get("city_gues")
    result = data["city_results"]
    num_photo = data["num_photo"]

    await message.answer("Спасибо за ваши ответы! Ищем ....")
    hotels = search_hotels(result[city_gues]["gaiaId"], num_res)
    print(hotels)

    if result:
        for hotel in hotels:
            if not need_photo:
                await bot.send_message(chat_id=message.from_user.id, text=f'hotel: {hotel["name"]}')
            else:
                images = get_hotel_images(hotel_id=str(hotel['id']), photo_limit=num_photo)
                for image in images:
                    await bot.send_photo(chat_id=message.chat.id, photo=image["url"], caption=hotel["name"])
                print(images)
    else:
        await message.answer("По запросу ничего не найдено")
    await state.reset_state(with_data=False)


def search_locations(city: str) -> list:
    params = {'q': city, 'locale': 'en_US'}
    response = api_request(method_endswith='locations/v3/search', params=params, method_type='GET')

    result = []
    if "sr" in response:
        search_results = response["sr"]
        if search_results:
            for entry in search_results:
                if "gaiaId" in entry:
                    region = {
                        "name": entry["regionNames"]["fullName"],
                        "gaiaId": entry["gaiaId"],
                    }
                    result.append(region)

    return result


def search_hotels(region: str, limit: int) -> list:
    today = datetime.date.today()
    start_date = today + datetime.timedelta(days=1)
    end_date = today + datetime.timedelta(days=5)
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {
            "regionId": region
        },
        "checkInDate": {
            "day": int(start_date.strftime("%d")),
            "month": int(start_date.strftime("%m")),
            "year": int(start_date.strftime("%Y"))
        },
        "checkOutDate": {
            "day": int(end_date.strftime("%d")),
            "month": int(end_date.strftime("%m")),
            "year": int(end_date.strftime("%Y"))
        },
        "rooms": [{"adults": 1}],
        "resultsStartingIndex": 0,
        "resultsSize": limit,
        "sort": "PRICE_LOW_TO_HIGH",
    }

    response = api_request(method_endswith='properties/v2/list', params=payload, method_type='POST')

    result = []
    if 'data' not in response:
        return result
    data = response["data"]

    if "propertySearch" in data:
        search_results = data["propertySearch"]["properties"]
        if search_results:
            for entry in search_results:
                hotel = {
                    "id": entry["id"],
                    "name": entry["name"],
                    "image": ""
                }
                if entry["propertyImage"] and "url" in entry["propertyImage"]["image"]:
                    hotel["image"] = entry["propertyImage"]["image"]["url"]

                result.append(hotel)

    return result


def get_hotel_images(hotel_id: str, photo_limit: int) -> list:
    images = []
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    print(payload)
    response = api_request(method_endswith='properties/v2/detail', params=payload, method_type='POST')
    print(response)
    data = response["data"]
    num_photo = 1
    if "propertyInfo" in data:
        gallery = data["propertyInfo"]["propertyGallery"]["images"]
        if gallery:
            for entry in gallery:
                image = {
                    "url": entry['image']['url']
                }
                images.append(image)
                num_photo += 1
                if num_photo > photo_limit:
                    break
    return images
