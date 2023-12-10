import os

from src.reports import spending_by_category
from src.utils import get_data_from_excel

# Получение пути к текущему исполняемому файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir[: -(len(current_dir.split("\\")[-1]) + 1)]

# Создание относительного пути к файлу от текущего файла
file_path_1 = os.path.join(base_dir, "tests", "for_tests_excel.xlsx")
DATE = "2021-12-31 16:44:00"  # нужный формат даты 'YYYY-MM-DD HH:MM:SS'
CATEGORY = "Фастфуд"

data = get_data_from_excel(file_path_1)


def test_spending_by_category():
    assert spending_by_category(data, CATEGORY, DATE).iloc[0, 4] == -120.00
