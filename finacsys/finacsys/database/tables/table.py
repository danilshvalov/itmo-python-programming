"""Модуль, содержащий реализацию основной структуры данных для БД"""
from typing import Dict, Callable, List
from uuid import UUID

from finacsys.models import Object


class Table(Dict[UUID, Object]):
    """Класс, реализующий основную функциональность таблиц базы данных"""

    def to_list(self) -> List[Object]:
        """Получение значений таблицы в виде списка"""
        return list(self.values())

    def pop_by(self, func: Callable[[Object], bool]) -> List[Object]:
        """Удаление элементов по предикативной функции"""
        will_be_removed = filter(func, self.values())
        will_be_removed = list(will_be_removed)

        for product in will_be_removed:
            self.pop(product.get_id())

        return will_be_removed

    def pop_by_name(self, name: str) -> List[Object]:
        """Удаление элементов, имя которых совпадает с переданным именем"""
        removed = self.pop_by(lambda object: object.get_name() == name)
        return removed
