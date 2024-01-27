"""Модуль, включающий в себя различные утилиты"""
from InquirerPy import inquirer


def confirm_sort() -> bool:
    """
    Подтверждение сортировки. Считывает решение пользователя с консоли.
    Возвращает булево значение
    """
    message = "Отсортировать результат?"
    result = inquirer.confirm(message=message).execute()
    return result


def confirm_reverse_sort() -> bool:
    """
    Подтверждение обратной сортировки. Считывает решение пользователя с
    консоли. Возвращает булево значение
    """
    message = "Отсортировать в обратном порядке?"
    result = inquirer.confirm(message=message).execute()
    return result


def confirm_write_to_file() -> bool:
    """
    Подтверждение записи в файл. Считывает решение пользователя с
    консоли. Возвращает булево значение
    """
    message = "Записать результат в файл?"
    result = inquirer.confirm(message=message).execute()
    return result
