"""Модуль, содержащий в себе модель товара"""
import uuid
from typing import Set, List

from .category import Category
from .object import ObjectMeta


class Product(ObjectMeta):
    """Класс, реализующий модель товара"""

    def __init__(self, name: str, price: float, categories: list[Category]):
        self.__name = name
        self.__price = price
        self.__categories = set(categories)
        self.__id = uuid.uuid4()

    def get_name(self) -> str:
        """Получение имени товара"""
        return self.__name

    def set_name(self, name: str):
        """Изменение имени товара. Имя не может быть пустой строкой"""
        if len(name) == 0:
            raise ValueError("Name cannot be an empty string")

        self.__name = name

    def get_price(self) -> float:
        """Получение стоимости товара"""
        return self.__price

    def set_price(self, value: float):
        """
        Изменение стоимости товара. Новая стоимость не может быть меньше или равна нулю
        """
        if value <= 0:
            raise ValueError("Price cannot be less than or equal to zero")

        self.__price = value

    def get_id(self) -> uuid.UUID:
        """Получение ID товара"""
        return self.__id

    def get_categories(self) -> Set[Category]:
        """Получение категорий товара"""
        return self.__categories

    def add_category(self, category: Category):
        """Добавление одной категории к категориям товара"""
        self.__categories.add(category)

    def add_categories(self, categories: List[Category]):
        """Добавление списка категорий к категориям товара"""

        for category in categories:
            self.add_category(category)

    def remove_category(self, category: Category):
        """Удаление категории из категорий товара"""
        self.__categories.discard(category)

    def remove_categories(self, categories: List[Category]):
        """Удаление списка категорий из категорий товара"""
        for category in categories:
            self.remove_category(category)

    def __str__(self):
        return f"{self.__id} | {self.__name} | {self.__price}"
