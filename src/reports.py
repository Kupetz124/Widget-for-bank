import datetime as dt
from typing import Optional

import pandas as pd

from src.decorators import log

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


@log("reports")
def spending_by_category(df: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date_now = dt.datetime.now().strftime("%d.%m.%Y")
    else:
        date_now = dt.datetime.strptime(date, "%d.%m.%Y").strftime("%d.%m.%Y")

    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)

    df["Starting_date"] = pd.to_datetime(date_now, dayfirst=True) - pd.DateOffset(months=3)
    df["Finish_date"] = pd.to_datetime(date_now, dayfirst=True)

    df = df[
        (df["Дата платежа"] >= df.Starting_date)
        & (df["Дата платежа"] <= df.Finish_date)
        & df["Категория"].str.contains(category)
    ]
    # df = df.groupby("Категория", as_index=False).agg({'Сумма платежа': 'sum'})

    return df
