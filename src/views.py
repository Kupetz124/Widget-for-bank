from typing import Any

import pandas as pd

from src.parsers import parser_currency

# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)


def convert_currencies(x: pd.DataFrame) -> Any:
    """Конвертирует валюту внутри DataFrame"""
    currency = x.Pay_currency
    if currency != "RUB":
        rate = parser_currency([currency])
        res = x.Total_spent * rate[currency]
    else:
        res = x.Total_spent
    return res


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Преобразовывает и сортирует данные из файла в удобный вид.
    :param df: DataFrame с транзакциями.
    :return: DataFrame с данными.
    """

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
    new_columns: Any = ["Date", "Card", "Status", "Pay_currency", "Total_spent", "Category", "Description", "Cashback"]
    df.columns = new_columns

    # Удаляем операции не по карте, операции пополнения карты и невыполненные операции.
    df = df[(df.Card.notnull()) & (df.Total_spent < 0) & (df.Status == "OK")]

    # Конвертируем платежи в других валютах в рубли.
    df.loc[:, "Total_spent"] = df.apply(convert_currencies, axis=1)
    df.loc[df.Pay_currency != "RUB", "Pay_currency"] = "RUB"

    # Округляем данные до двух знаков после запятой.
    df = df.apply(lambda x: round(x, 2) if x.dtypes == "float64" else x)
    return df


def get_monthly_data(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """
    Возвращает транзакции за календарный месяц, совпадающий с указанной датой.
    :param df: DataFrame с транзакциями.
    :param date: Строка с датой в формате 'YYYY-MM-DD HH:MM:SS'.
    :return:DataFrame с транзакциями за указанный месяц.
    """

    sample = date[5:7] + "." + date[:4]

    return df[df["Дата операции"].str.contains(sample)]


def get_statistics(data: pd.DataFrame) -> list[dict]:
    """
    Выводит статистику затрат по картам и рассчитывает кэшбэк.

    :param data: DataFrame с транзакциями
    :return: Dict со статистикой
    """

    cards = data.groupby("Card", as_index=False)
    df = cards.agg({"Total_spent": "sum", "Cashback": "sum"})

    df.Cashback += round(abs(df.Total_spent / 100), 2)

    # Округляем данные до двух знаков после запятой.
    df = df[["Card", "Total_spent", "Cashback"]].apply(lambda x: round(x, 2) if x.dtypes == "float64" else x)

    return df.to_dict("records")


def get_top_five(data: pd.DataFrame) -> list[dict]:
    """
    Возвращает топ-5 наибольших затрат.
    :param data: DataFrame с транзакциями.
    :return: DataFrame с топ-5 по затратам транзакциями.
    """

    data = data[["Date", "Card", "Total_spent", "Category", "Description"]].sort_values("Total_spent")

    return data.head().to_dict("records")
