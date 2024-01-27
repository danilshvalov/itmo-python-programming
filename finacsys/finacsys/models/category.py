"""Модуль, содержащий в себе модель категорий"""
import uuid
from .object import ObjectMeta


class Category(ObjectMeta):
    """Модель категории"""

    def __init__(self, name: str):
        self.__name = name
        self.__id = uuid.uuid4()

    def __str__(self) -> str:
        return f"ID: {self.__id}, название: {self.__name}"

    def __repr__(self) -> str:
        return self.__str__()

    def get_id(self) -> uuid.UUID:
        """Получение ID категории"""
        return self.__id

    def get_name(self) -> str:
        """Получение имени категории"""
        return self.__name

    def set_name(self, value: str):
        """
        Изменение имени категории. Новое имя не может быть пустой строкой
        """
        if len(value) == 0:
            raise ValueError("Name cannot be an empty string")

        self.__name = value
