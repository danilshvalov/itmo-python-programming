"""Утилиты для реализации CLI-представления"""
from typing import List

from finacsys.models import Category
from finacsys.utils import make_str_table


def make_table(expenses: List[Category]) -> str:
    """Создание таблицы в виде строки, где каждый столбец соответствует
    определенному полю модели Category.

    Args:
        expenses (List[Category]): список данных для таблицы

    Returns:
        str: таблица в виде строки
    """
    header = [["ID", "Название"]]
    rows = [[e.get_id(), e.get_name()] for e in expenses]

    table = make_str_table(header, rows)
    return table
