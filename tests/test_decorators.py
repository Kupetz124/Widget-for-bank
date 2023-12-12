import os

import pytest

from src.decorators import log
from src.utils import get_data_from_excel


@pytest.fixture
def data():
    # Получение пути к текущему исполняемому файлу
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = current_dir[: -(len(current_dir.split("\\")[-1]) + 1)]

    # Создание относительного пути к нужному файлу от текущего файла
    file_path = os.path.join(base_dir, "tests", "for_tests_Excel.xlsx")

    return get_data_from_excel(file_path)


def test_log(data):
    @log()
    def func(x):
        return x

    assert func(data).loc[1, "Сумма платежа"] == -64
