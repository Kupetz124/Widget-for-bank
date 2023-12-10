import os

from src.services import search_string
from src.utils import get_data_from_excel

# Получение пути к текущему исполняемому файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir[: -(len(current_dir.split("\\")[-1]) + 1)]

# Создание относительного пути к файлу от текущего файла
file_path_1 = os.path.join(base_dir, "tests", "for_tests_excel.xlsx")

# получение тестовых данных
data = get_data_from_excel(file_path_1)

SEARCH_STRING = "Mitrankov"


def test_spending_by_category():
    assert search_string(data, SEARCH_STRING).iloc[0, 4] == -349.00
