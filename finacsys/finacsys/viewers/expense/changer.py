"""Модуль, содержащий CLI-фронтенд для изменения расходов"""
from typing import Callable, List
from enum import Enum

from finacsys.models import Expense

from ..viewer import Viewer


class Action(Enum):
    """Действия, доступные пользователю для изменения расходов"""

    EXIT = "Назад"
    CHANGE_DATE = "Изменить дату"
    CHANGE_TIME = "Изменить время"
    CHANGE_PRODUCT = "Изменить товар"
    CHANGE_COUNT = "Изменить количество"

    def __str__(self) -> str:
        return self.value


class ExpenseChangerViewer(Viewer):
    """CLI-фронтенд для предоставления изменения расходов"""

    def __select_action(self) -> Action:
        message = "Выберите действие"
        choices = list(Action)
        action: Action = super().select(message=message, choices=choices)
        return action

    def __change_product(self, expenses: Expense):
        message = "Выберите товар"
        product = self.select_product(message=message)
        expenses.set_product(product)

    def __change_count(self):
        count = super().read_count()
        return lambda expense: expense.set_count(count)

    def __change_time(self):
        time = super().read_time()
        return lambda expense: expense.set_time(time)

    def __change_date(self):
        date = super().read_date()
        return lambda expense: expense.set_date(date)

    def __dispact_action(self, action: Action) -> Callable[[Expense], None]:
        if action == Action.CHANGE_DATE:
            return self.__change_date()
        if action == Action.CHANGE_TIME:
            return self.__change_time()
        if action == Action.CHANGE_PRODUCT:
            return self.__change_product
        if action == Action.CHANGE_COUNT:
            return self.__change_count()
        raise NotImplementedError()

    def attach(self, expenses: List[Expense]):
        """Присоединение CLI-фронтенда к консоли"""
        while True:
            action = self.__select_action()
            action = self.__dispact_action(action)

            if action == Action.EXIT:
                break

            for expense in expenses:
                action(expense)
