import os
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd


def log(file_name: Optional[str] = None) -> Any:
    """
    Записывает результат работы функции в excel файл.
    :param file_name: Путь к файлу с логами, если не указан, то идёт вывод в файл по умолчанию.
    :return: Результат работы функции.
    """

    def wrapper(func: Callable) -> Any:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            # Получение пути к текущему исполняемому файлу
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = current_dir[: -(len(current_dir.split("\\")[-1]) + 1)]

            # проверяем, указан ли файл для логов, если нет, записываем в файл по умолчанию.
            if file_name is None:
                my_file = os.path.join(base_dir, "data", "my_reports.xlsx")
            else:
                my_file = os.path.join(base_dir, "data", f"{file_name}.xlsx")

            result = func(*args, **kwargs)

            # Записываем результат работы функции в файл.
            with pd.ExcelWriter(
                my_file,
                mode="w",
            ) as writer:
                result.to_excel(writer)

            # Выводим результат работы декорируемой функции
            return result

        return inner

    return wrapper
