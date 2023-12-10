import json
import os
from typing import Any, Iterable, Optional

from src.parsers import parser_currency, parser_stocks
from src.reports import spending_by_category
from src.services import search_string
from src.utils import get_data_from_excel, greet_user, read_json
from src.views import get_monthly_data, get_statistics, get_top_five, prepare_data

PATH_FILE = os.path.join("..", "data", "operations.xls")
DATE = "2021-12-31 16:44:00"  # нужный формат даты 'YYYY-MM-DD HH:MM:SS'
CATEGORY = "Супермаркеты"
SEARCH = "Каршеринг"
USER_SETTINGS = os.path.join("..", "data", "user_settings.json")


def main(path_file: str, date_str: str, user_settings: Any, search_row: Optional[None | str] = None) -> Iterable:
    """
    Основная логика программы.
    :param path_file: Путь к файлу excel с историей транзакций.
    :param date_str: Дата от которой мы хотим анализировать данные за месяц.
    :param user_settings: Путь к файлу с настройками пользователя.
    :param search_row:Поисковая строка для поиска в общем файле транзакций
    :return: json с аналитическими данными пользователя.
    """

    # Считываем данные из файла.
    extracted_data = get_data_from_excel(path_file)

    # Отбираем транзакции за месяц от указанной даты.
    monthly_data = get_monthly_data(extracted_data, date_str)

    # Если поисковая строка задана, выбираем транзакции,
    # содержащие поисковую строку, за месяц и записываем их в excel файл.
    if search_row is not None:
        search_string(monthly_data, search_row)

    # записываем в файл отчёт о тратах по выбранной категории за три месяца от заданной даты.
    spending_by_category(extracted_data, CATEGORY, date_str)

    # Приводим данные в нужный нам формат.
    cleared_data = prepare_data(monthly_data)

    # приветствие пользователя
    greeting = greet_user()

    # получение статистики
    cards = get_statistics(cleared_data)
    top_costs = get_top_five(cleared_data)

    # получение настроек пользователя
    user_settings = read_json(user_settings)

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
    print(main(PATH_FILE, DATE, USER_SETTINGS, SEARCH))
