"""Модуль, содержащий в себе различные валидаторы"""
from pathlib import Path
import datetime as dt
from InquirerPy.validator import Validator, ValidationError
from prompt_toolkit.document import Document

import finacsys.config as cfg


class DateValidator(Validator):
    """
    Валидатор дат. Валидация происходит в соответствии с форматом дат.
    Формат дат импортируется из finacsys.config.
    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def validate(self, document: Document):
        try:
            dt.datetime.strptime(document.text.strip(), cfg.DATE_FORMAT)
        except ValueError as error:
            raise ValidationError(
                message=self.message, cursor_position=document.cursor_position
            ) from error


class TimeValidator(Validator):
    """
    Валидатор времени. Валидация происходит в соответствии с форматом времени.
    Формат времени импортируется из finacsys.config.
    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def validate(self, document: Document) -> None:
        try:
            dt.datetime.strptime(document.text.strip(), cfg.TIME_FORMAT)
        except ValueError as error:
            raise ValidationError(
                message=self.message,
                cursor_position=document.cursor_position,
            ) from error


class FileValidator(Validator):
    """
    Валидатор пути файлов. Выбрасывает исключение только в том случае, если
    указанный файл (существующему или несуществующему) является директорией.
    """

    def __init__(
        self,
        message: str = "Input is not a valid path",
    ) -> None:
        """Set invalid message and check condition."""
        self.message = message

    def validate(self, document) -> None:
        """Check if user input filepath exists based on condition."""
        path = Path(document.text).expanduser()

        if path.is_dir():
            raise ValidationError(
                message=self.message,
                cursor_position=document.cursor_position,
            )


class NumberValidator(Validator):
    """Проверяет число на натуральность. Число может быть как целым, так и
    дробным. Число может равняться нулю.
    """

    def __init__(self, message: str = "Цена должна быть натуральным числом"):
        self.message = message

    def validate(self, document: Document):
        try:
            number = float(document.text)
            if number < 0:
                raise ValueError()
        except ValueError as error:
            raise ValidationError(
                message=self.message,
                cursor_position=document.cursor_position,
            ) from error
