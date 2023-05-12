from requests import get, post
import requests
from config_data import config
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import datetime
from loader import bot


def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    if method_type == 'GET':
        return get_request(
            url=url,
            params=params,
            headers=headers
        )
    else:
        return post_request(
            url=url,
            params=params,
            headers=headers
        )


def get_request(url, params, headers):
    try:
        response = get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.json()
    except ValueError as error:
        print('Ошибка приложения: ' + str(error))


def post_request(url, params, headers):
    try:
        headers["content-type"] = "application/json"
        response = post(
            url,
            headers=headers,
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
    result = data.get("city_results")
    num_photo = data.get("num_photo")
    sort = data.get('sort')

    await message.answer("Спасибо за ваши ответы! Ищем ....")
    hotels = search_hotels(result[city_gues]["gaiaId"], num_res, sort)
    print(hotels)

    if result:
        for hotel in hotels:
            if not need_photo:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f'hotel: {hotel["name"]} price: {hotel["price"]}')
            else:
                images = get_hotel_images(hotel_id=str(hotel['id']), photo_limit=num_photo)
                for image in images:
                    await bot.send_photo(chat_id=message.chat.id, photo=image["url"],
                                         caption=f'hotel: {hotel["name"]} price: {hotel["price"]}')
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


def search_hotels(region: str, limit: int, sort: str = 'l2h') -> list:
    today = datetime.date.today()
    start_date = today + datetime.timedelta(days=1)
    end_date = today + datetime.timedelta(days=5)

    if sort == 'l2h':
        request_limit = limit
    else:
        request_limit = 200

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
        "resultsSize": request_limit,
        "sort": "PRICE_LOW_TO_HIGH",
    }

    response = api_request(method_endswith='properties/v2/list', params=payload, method_type='POST')

    result = []
    if 'data' not in response:
        return result
    data = response["data"]

    hotels_counter = 0
    if "propertySearch" in data:
        hotels = data["propertySearch"]["properties"]
        if hotels:
            if sort != 'l2h':
                hotels = hotels[::-1]

            for entry in hotels:
                if hotels_counter <= limit:
                    hotel = {
                        "id": entry["id"],
                        "name": entry["name"],
                        "image": "",
                        "price": entry['price']["lead"]["formatted"]
                    }
                    if entry["propertyImage"] and "url" in entry["propertyImage"]["image"]:
                        hotel["image"] = entry["propertyImage"]["image"]["url"]

                    result.append(hotel)
                    hotels_counter += 1

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

    response = api_request(method_endswith='properties/v2/detail', params=payload, method_type='POST')

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
