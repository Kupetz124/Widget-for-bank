import json
import os
from datetime import datetime
from typing import Any

import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


def greet_user() -> str:
    """
    Формирует приветствие в зависимости от времени суток.
    :return:
    """
    time_now = datetime.now().hour

    if 0 <= time_now < 6:
        return "Доброй ночи!"
    elif 6 <= time_now < 12:
        return "Доброе утро!"
    elif 12 <= time_now < 18:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def read_json() -> Any:
    """
    Считывает настройки пользователя из json файла и возвращает словарь с ними.
    :return: Словарь с настройками пользователя.
    """
    with open(os.path.join("..", "data", "user_settings.json")) as file:
        return json.load(file)
