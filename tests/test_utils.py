import os
from datetime import datetime
from unittest.mock import patch

from src.utils import get_data_from_excel, greet_user, read_json

# Получение пути к текущему исполняемому файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir[: -(len(current_dir.split("\\")[-1]) + 1)]

# Создание относительного пути к файлу от текущего файла
file_path_1 = os.path.join(base_dir, "data", "transactions_excel.xlsx")
file_path_2 = os.path.join(base_dir, "data", "user_settings.json")


@patch("pandas.read_excel")
def test_get_data_from_excel(mock_get):
    mock_get.return_value = ["name", "price", "quantity"]
    assert get_data_from_excel(file_path_1) == ["name", "price", "quantity"]


@patch("json.load")
def test_read_json(mock_get):
    mock_get.return_value = {"USD": 90}
    assert read_json(file_path_2) == {"USD": 90}


def test_greet_user():
    time_now = datetime.now().hour

    if 0 <= time_now < 6:
        answer = "Доброй ночи!"
    elif 6 <= time_now < 12:
        answer = "Доброе утро!"
    elif 12 <= time_now < 18:
        answer = "Добрый день!"
    else:
        answer = "Добрый вечер!"

    assert greet_user() == answer
