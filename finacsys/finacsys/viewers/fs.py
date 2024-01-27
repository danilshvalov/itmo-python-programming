"""Модуль, включающий в себя CLI-фронтенд для запросов к файловой системе"""
from pathlib import Path
from InquirerPy import inquirer

from finacsys.validator import FileValidator


def read_filename() -> Path:
    """Чтение имени файла с консоли"""
    message = "Введите имя файла"
    error = "Выберите другое имя файла"

    filename = inquirer.filepath(
        message=message,
        validate=FileValidator(message=error),
    ).execute()

    filename = Path(filename).expanduser()

    return filename


def write_to_file(value: str):
    """
    Запись строки в файл. Перед записью запрашивать у пользователя имя файла,
    после чего считывает имя файла с консоли
    """
    filename = read_filename()
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(value)


def confirm_write_to_file() -> bool:
    """
    Подтверждение записи в файл. Ответ возвращается в виде булевого значения
    """
    message = "Записать результат в файл?"
    result = inquirer.confirm(message=message).execute()
    return result
