"""Модуль с CLI-фронтендом для сортировки товаров"""

from typing import List
from enum import Enum

from finacsys.models import Category
from finacsys.database import Database
from finacsys.viewers.utils import confirm_reverse_sort

from ..viewer import Viewer


class Action(Enum):
    """Действия сортировки, доступные пользователю"""

    STOP_SORTING = "Закончить сортировку"
    SORT_BY_NAME = "Отсортировать по имени категории"

    def __str__(self) -> str:
        return self.value


class CategorySorterViewer(Viewer):
    """Класс, предоставляющий CLI-фронтенд"""

    def __init__(self, database: Database):
        super().__init__(database)
        self.sorted_expenses = []

    def __read_action(self):
        message = "Выберите действие"
        choices = list(Action)
        action = super().select(message=message, choices=choices)
        return action

    def __sort_by_name(self, reverse):
        self.sorted_expenses.sort(
            key=lambda exp: exp.get_name(),
            reverse=reverse,
        )

    def attach(self, expenses: List[Category]) -> List[Category]:
        """Присоединение CLI-фронтенда к консоли"""
        self.sorted_expenses = expenses

        while True:
            action = self.__read_action()

            if action == Action.STOP_SORTING:
                return self.sorted_expenses

            is_reverse = confirm_reverse_sort()

            if action == Action.SORT_BY_NAME:
                self.__sort_by_name(is_reverse)
