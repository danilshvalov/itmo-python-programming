"""Утилиты для реализации CLI-представления"""
from typing import List

from finacsys.models import Expense
from finacsys.utils import make_str_table


def make_table(expenses: List[Expense]) -> str:
    """Создание таблицы в виде строки, где каждый столбец соответствует
    определенному полю модели Expense.

    Args:
        expenses (List[Expense]): список данных для таблицы

    Returns:
        str: таблица в виде строки
    """
    header = [["ID", "Название", "Количество", "Общая цена", "Дата", "Время"]]
    rows = [
        [
            e.get_id(),
            e.get_name(),
            str(e.get_count()),
            str(e.get_price()),
            e.get_date().strftime("%d.%m.%Y"),
            e.get_time().strftime("%H:%M:%S"),
        ]
        for e in expenses
    ]

    table = make_str_table(header, rows)
    return table
