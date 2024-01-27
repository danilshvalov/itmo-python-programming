"""Модуль, содержащий в себе абстрактный класс модели объектов"""
from uuid import UUID
from typing import TypeVar


class ObjectMeta:
    """Абстрактный класс объекта базы данных"""

    def get_id(self) -> UUID:
        """Получение ID. Класс-наследник должен переопределить этот метод"""
        raise NotImplementedError()

    def get_name(self) -> str:
        """
        Получение названия. Класс-наследник должен переопределить этот метод
        """
        raise NotImplementedError()


Object = TypeVar("Object", bound=ObjectMeta)
