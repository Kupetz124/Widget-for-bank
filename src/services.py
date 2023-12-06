import pandas as pd


def search_string(path: str, row: str) -> pd.DataFrame:
    """
    Возвращает DataFrame с транзакциями, в описании или категории которых есть искомая строка.
    :param path: Путь к файлу с транзакциями.
    :param row:Искомая строка или слово.
    :return: DataFrame с транзакциями, содержащими искомую строку.
    """

    df = pd.read_excel(path)
    df = df[df["Описание"].str.contains(row) | df["Категория"].str.contains(row)]

    return df
