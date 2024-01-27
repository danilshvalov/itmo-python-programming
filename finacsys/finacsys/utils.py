"""Модуль, содержащий различные функции-утилиты"""
from typing import List
from texttable import Texttable


def make_str_table(header: List[List[str]], rows: List[List[str]]) -> str:
    """Создание таблицы в строковом представлении

    Args:
        header (List[List[str]]): заголовок таблицы
        rows (List[List[str]]): строки таблицы

    Returns:
        str: таблица в виде строки
    """
    table = Texttable()
    table.add_rows(header + rows)

    result = table.draw()
    if result is None:
        raise RuntimeError("Table cannot be created")

    return result
