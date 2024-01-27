"""Модуль с CLI-фронтендом для сортировки списка расходов"""

from typing import List
from enum import Enum

from finacsys.models import Expense
from finacsys.database import Database
from finacsys.viewers.utils import confirm_reverse_sort

from ..viewer import Viewer


class Action(Enum):
    """Действия сортировки, доступные пользователю"""

    STOP_SORTING = "Закончить сортировку"
    SORT_BY_DATE = "Отсортировать по дате"
    SORT_BY_TIME = "Отсортировать по времени"
    SORT_BY_PRODUCT_PRICE = "Отсортировать по цене товара"
    SORT_BY_TOTAL_PRICE = "Отсортировать по итоговой цене"
    SORT_BY_NAME = "Отсортировать по имени товара"

    def __str__(self) -> str:
        return self.value


class ExpenseSorterViewer(Viewer):
    """Класс, предоставляющий CLI-фронтенд"""

    def __init__(self, database: Database):
        super().__init__(database)
        self.sorted_expenses = []

    def __read_action(self):
        message = "Выберите действие"
        choices = list(Action)
        action = super().select(message=message, choices=choices)
        return action

    def __sort_by_date(self, reverse):
        self.sorted_expenses.sort(
            key=lambda exp: exp.get_date(),
            reverse=reverse,
        )

    def __sort_by_time(self, reverse):
        self.sorted_expenses.sort(
            key=lambda exp: exp.get_time(),
            reverse=reverse,
        )

    def __sort_by_product_price(self, reverse):
        self.sorted_expenses.sort(
            key=lambda exp: exp.get_price(),
            reverse=reverse,
        )

    def __sort_by_total_price(self, reverse):
        self.sorted_expenses.sort(
            key=lambda exp: exp.get_total_price(),
            reverse=reverse,
        )

    def __sort_by_name(self, reverse):
        self.sorted_expenses.sort(
            key=lambda exp: exp.get_name(),
            reverse=reverse,
        )

    def attach(self, expenses: List[Expense]) -> List[Expense]:
        """Присоединение CLI-фронтенда к консоли"""
        self.sorted_expenses = expenses

        while True:
            action = self.__read_action()

            if action == Action.STOP_SORTING:
                return self.sorted_expenses

            is_reverse = confirm_reverse_sort()

            if action == Action.SORT_BY_DATE:
                self.__sort_by_date(is_reverse)
            elif action == Action.SORT_BY_TIME:
                self.__sort_by_time(is_reverse)
            elif action == Action.SORT_BY_NAME:
                self.__sort_by_name(is_reverse)
            elif action == Action.SORT_BY_PRODUCT_PRICE:
                self.__sort_by_product_price(is_reverse)
            elif action == Action.SORT_BY_TOTAL_PRICE:
                self.__sort_by_total_price(is_reverse)
