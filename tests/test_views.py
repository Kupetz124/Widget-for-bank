import os
from unittest.mock import patch

import pytest

from src.utils import get_data_from_excel
from src.views import convert_currencies, get_monthly_data, get_statistics, get_top_five, prepare_data

# Получение пути к текущему исполняемому файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir[: -(len(current_dir.split("\\")[-1]) + 1)]

# Создание относительного пути к файлу от текущего файла
file_path = os.path.join(base_dir, "tests", "for_tests_Excel.xlsx")

DF = get_data_from_excel(file_path)
DATE = "2021-12-31 16:44:00"  # нужный формат даты 'YYYY-MM-DD HH:MM:SS'


@pytest.fixture
def data():
    df = get_data_from_excel(file_path)

    # Отфильтровываем ненужные столбцы
    list_columns = [
        "Дата платежа",
        "Номер карты",
        "Статус",
        "Валюта платежа",
        "Сумма платежа",
        "Категория",
        "Описание",
        "Бонусы (включая кэшбэк)",
    ]
    df = df[list_columns]

    # Переименовываем названия столбцов
    new_columns = ["Date", "Card", "Status", "Pay_currency", "Total_spent", "Category", "Description", "Cashback"]
    df.columns = new_columns

    return df


def test_convert_currencies(data):
    with patch("src.views.parser_currency") as mock_get:
        mock_get.return_value = {"USD": 100}
        assert round(convert_currencies(data.iloc[0, :])) == -16089


def test_prepare_data():
    assert prepare_data(DF).loc[0, "Cashback"] == 3


def test_get_monthly_data():
    assert get_monthly_data(DF, DATE).loc[0, "Сумма платежа"] == -160.89


def test_get_statistics(data):
    test = get_statistics(data)
    assert test[0]["Cashback"] == 1902.23


def test_get_top_five(data):
    assert get_top_five(data)[0]["Total_spent"] == -20000
