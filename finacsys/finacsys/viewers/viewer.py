"""Модуль, содержащий в себе общий класс для создания Viewer-ов"""
from typing import Any
import datetime as dt
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from finacsys.database import Database
from finacsys.validator import DateValidator, TimeValidator, NumberValidator
import finacsys.config as cfg


class Viewer:
    """Класс с основной функциональностью CLI-интерфейса"""

    def __init__(self, database: Database):
        self.database = database

    def select(self, message: str, choices: Any) -> Any:
        """Выбор единственного элемента из переданного списка

        Args:
            message (str): сообщение, выводимое на экран
            choices (Any): список, предлагаемый пользователю для выбора

        Returns:
            Any: единственный элемент из переданного списка
        """
        assert len(choices) > 0

        message = f"{message}\nДля выбора используйте Enter"

        result = inquirer.fuzzy(message=message, choices=choices).execute()
        return result

    def multiselect(self, message: str, choices: Any) -> Any:
        """Выбор одного или нескольких элементов из переданного списка

        Args:
            message (str): сообщение, выводимое на экран
            choices (Any): список, предлагаемый пользователю для выбора

        Returns:
            Any: Список элементов, выбранных пользователем
        """
        assert len(choices) > 0

        message = (
            f"{message}\nДля выбора используйте пробел, "
            "а для подтверждения — Enter"
        )

        result = inquirer.fuzzy(
            message=message,
            choices=choices,
            multiselect=True,
            validate=lambda res: len(res) > 0,
            invalid_message="Необходимо выбрать хотя бы 1 позицию",
        ).execute()

        return result

    def select_product(self, message: str, multiselect: bool = False):
        """Выбор товара, находящегося в базе данных.
        Доступен множественный выбор

        Args:
            message (str): сообщение, выводимое на экран
            multiselect (bool, optional): включение множественнего выбора.
            По умолчанию выключен

        Returns:
            Товар или список товаров (в зависимости от опции multiselect)
        """
        choices = self.database.get_products_list()

        if multiselect:
            return self.multiselect(message=message, choices=choices)

        return self.select(message=message, choices=choices)

    def select_category(self, message: str, multiselect: bool = False):
        """Выбор категории, находящейся в базе данных.
        Доступен множественный выбор

        Args:
            message (str): сообщение, выводимое на экран
            multiselect (bool, optional): включение множественнего выбора.
            По умолчанию выключен

        Returns:
            Категория или список категорий (в зависимости от опции multiselect)
        """
        choices = self.database.get_categories_list()

        if multiselect:
            return self.multiselect(message=message, choices=choices)

        return self.select(message=message, choices=choices)

    def select_expense(self, message: str, multiselect: bool = False):
        """Выбор статьи расхода, находящегося в базе данных.
        Доступен множественный выбор

        Args:
            message (str): сообщение, выводимое на экран
            multiselect (bool, optional): включение множественнего выбора.
            По умолчанию выключен

        Returns:
            Статья расхода или список расходов
            (в зависимости от опции multiselect)
        """
        choices = self.database.get_expenses_list()

        if multiselect:
            return self.multiselect(message=message, choices=choices)

        return self.select(message=message, choices=choices)

    def read_name(self) -> str:
        """Чтение имени. Вводимое имя не может быть пустым"""
        message = "Введите имя"
        validate = EmptyInputValidator("Имя не может быть пустым")
        name = inquirer.text(message=message, validate=validate).execute()
        return name

    def read_price(self) -> float:
        """Чтение значения цены. Цена не может быть меньше или равна нулю"""
        message = "Введите значение цены:"

        price = inquirer.text(
            message=message,
            validate=NumberValidator(),
        ).execute()
        return float(price)

    def read_count(self) -> float:
        """Чтение количества. Количество не может быть меньше или равно нулю"""
        message = "Введите количество:"
        price = inquirer.text(
            message=message,
            validate=NumberValidator(),
        ).execute()
        return float(price)

    def read_date(self) -> dt.date:
        """
        Чтение даты. Дата должна быть в формате, установленном в
        конфигурационном файле (см finacsys.config)
        """
        message = f"Введите дату в формате {cfg.CONSOLE_DATE_FORMAT}"
        error_message = "Проверьте формат даты и логическую корректность"

        date = inquirer.text(
            message=message,
            validate=DateValidator(message=error_message),
        ).execute()
        date = dt.datetime.strptime(date, cfg.DATE_FORMAT).date()
        return date

    def read_time(self) -> dt.time:
        """
        Чтение времени. Время должно быть в формате, установленном в
        конфигурационном файле (см finacsys.config)
        """
        message = f"Введите время в формате {cfg.CONSOLE_TIME_FORMAT}"
        error_message = "Проверьте формат времени и логическую корректность"

        time = inquirer.text(
            message=message,
            validate=TimeValidator(error_message),
        ).execute()
        time = dt.datetime.strptime(time, cfg.TIME_FORMAT).time()
        return time

    def read_datetime(self) -> dt.datetime:
        """
        Чтение даты и времени. Дата и время должны быть в формате,
        установленном в конфигурационном файле (см finacsys.config)
        """
        date = self.read_date()
        time = self.read_time()
        datetime = dt.datetime.combine(date, time)
        return datetime
