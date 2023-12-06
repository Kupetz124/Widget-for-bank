import json
import os
from typing import Iterable

from src.parsers import parser_currency, parser_stocks
from src.utils import greet_user, read_json
from src.views import get_monthly_data, get_statistics, get_top_five, prepare_data

PATH_FILE = os.path.join("..", "data", "operations.xls")
DATE = "2021-12-31 16:44:00"  # нужный формат даты 'YYYY-MM-DD HH:MM:SS'


def main(path_file: str, date_str: str) -> Iterable:
    # Извлечение и первичная обработка данных из файла.
    monthly_data = get_monthly_data(path_file, date_str)
    cleared_data = prepare_data(monthly_data)

    # приветствие пользователя
    greeting = greet_user()

    # получение статистики
    cards = get_statistics(cleared_data)
    top_costs = get_top_five(cleared_data)

    # получение настроек пользователя
    user_settings = read_json()

    # получение текущих курсов валют и ценных бумаг из настроек пользователя по API.

    required_currencies = parser_currency(user_settings["user_currencies"])
    required_stocks = parser_stocks(user_settings["user_stocks"])

    # формируем словарь с полученными данными.
    new_dict = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_costs,
        "currency_rates": required_currencies,
        "stock_prices": required_stocks,
    }

    # with open("file.json", "w", encoding="utf-8") as file:
    #     json.dump(new_dict, file, indent=4, ensure_ascii=False)

    # возвращаем словарь в формате json
    return json.dumps(new_dict, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(main(PATH_FILE, DATE))
