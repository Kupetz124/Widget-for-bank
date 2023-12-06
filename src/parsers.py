import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_STOCKS = os.getenv("API_KEY_ALFA")
API_KEY_CURRENCY = os.getenv("API_KEY_EXCHANGE")


def parser_stocks(list_stocks: list[str]) -> dict:
    """
    Получает данные акций по API.
    :param list_stocks:Список тикеров акций.
    :return:Словарь с ценами акций из списка.
    """
    # Запускаем цикл по списку акций, так как API возвращает данные по одной бумаге

    new_dict = {}

    for item in list_stocks:
        # параметры гет запроса:
        payload = {
            "function": "GLOBAL_QUOTE",
            "symbol": item,
            "apikey": API_KEY_STOCKS,
            "datatype": "json",
        }
        # Ссылка на ресурс и гет запрос:
        url = "https://www.alphavantage.co/query"
        res = requests.get(url, params=payload).json()

        # формирование словаря с данными по акциям.
        new_dict[item] = res["Global Quote"]["05. price"]

    return new_dict


def parser_currency(rate: list[Any]) -> dict:
    """
    Получает данные по курсу валют из списка.
    :param rate: Список нужных валют.
    :return: Словарь с курсом валют из списка относительно рубля.
    """
    # формируем строку для параметров гет запроса.
    line = " ".join(rate).replace(" ", ",")
    need_line = "symbols=RUB," + line

    # Параметры гет запроса.
    payload = {"app_id": API_KEY_CURRENCY}
    url = f"https://openexchangerates.org/api/latest.json?{need_line}"
    headers = {"accept": "application/json"}

    # гет запрос
    response = requests.get(url, headers=headers, params=payload).json()

    # пересчитываем в цикле курс валют относительно рубля, так как базовая валюта API запроса - 'USD'
    new_dict = {}

    for item in response["rates"]:
        if item == "USD":
            new_dict["USD"] = round(response["rates"]["RUB"], 2)
        else:
            new_dict[item] = round(response["rates"]["RUB"] / response["rates"][item], 2)

    del new_dict["RUB"]

    return new_dict
