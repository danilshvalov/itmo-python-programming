"""Модуль, включающий в себя модель расходов"""
import datetime as dt
import uuid
from typing import Set

from .product import Product
from .category import Category
from .object import ObjectMeta


class Expense(ObjectMeta):
    """Модель расходов"""

    def __init__(
        self, product: Product, count: float, created_at: dt.datetime
    ):
        self.__id = uuid.uuid4()
        self.__product = product
        self.__count = count
        self.__created_at = created_at

    def __str__(self):
        name = self.get_name()
        price = self.get_price()
        total_price = self.get_total_price()
        date = self.get_datetime().strftime("%H:%M:%S %d-%m-%Y")
        return (
            f"ID: {str(self.__id)}, название: {name}, количество: {price}, "
            + f"общая цена: {total_price}, дата: {date}"
        )

    def get_datetime(self) -> dt.datetime:
        """Получение даты и времени создания статьи расхода"""
        return self.__created_at

    def get_date(self) -> dt.date:
        """Получение даты создания статьи расхода"""
        return self.__created_at.date()

    def set_date(self, date: dt.date):
        """Изменение даты создания статьи расхода"""
        new_datetime = dt.datetime.combine(date, self.__created_at.time())
        self.__created_at = new_datetime

    def get_time(self) -> dt.time:
        """Получение времени создания статьи расхода"""
        return self.__created_at.time()

    def set_time(self, time: dt.time):
        """Изменение времени создания статьи расхода"""
        new_datetime = dt.datetime.combine(self.__created_at.date(), time)
        self.__created_at = new_datetime

    def get_price(self) -> float:
        """Получение стоимости товара"""
        return self.__product.get_price()

    def set_price(self, value: float):
        """
        Изменение стоимости товара, в том числе в базе данных. Новое значение
        стоимости не может быть меньше или равно нулю
        """
        if value <= 0:
            raise ValueError("Price cannot be less than or equal to zero")

        self.__product.set_price(value)

    def get_name(self) -> str:
        """Получение названия товара"""
        return self.__product.get_name()

    def get_count(self) -> float:
        """Получение количества товара"""
        return self.__count

    def set_count(self, value: float):
        """
        Изменение количества товара. Новое значение стоимости не может быть
        меньше или равно нулю
        """
        if value <= 0:
            raise ValueError("Count cannot be less than or equal to zero")
        self.__count = value

    def get_product_id(self) -> uuid.UUID:
        """Получение ID товара"""
        return self.__product.get_id()

    def set_product(self, product: Product):
        """Замена с одного товара на другой"""
        self.__product = product

    def get_categories(self) -> Set[Category]:
        """Получение категорий товара"""
        return self.__product.get_categories()

    def get_id(self) -> uuid.UUID:
        """Получение ID статьи расхода"""
        return self.__id

    def get_total_price(self):
        """
        Вычисление итоговой цены. Итоговая цена вычисляется по формуле:
        TOTAL PRICE = COUNT * PRICE
        """
        return self.get_count() * self.get_price()

    def __repr__(self) -> str:
        return self.__str__()
