import pandas as pd

from src.decorators import log


@log("my_search")
def search_string(df: pd.DataFrame, row: str) -> pd.DataFrame:
    """
    Возвращает DataFrame с транзакциями, в описании или категории которых есть искомая строка.
    :param df: DataFrame с транзакциями.
    :param row:Искомая строка или слово.
    :return: DataFrame с транзакциями, содержащими искомую строку.
    """

    df = df[df["Описание"].str.contains(row) | df["Категория"].str.contains(row)]

    return df
