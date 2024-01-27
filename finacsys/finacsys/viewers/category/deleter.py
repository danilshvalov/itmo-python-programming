"""Модуль с CLI-фронтендом, представляющим удаление категорий"""

from enum import Enum
from typing import List

from finacsys.models import Category

from ..viewer import Viewer


class Action(Enum):
    """Способы удаления категории"""

    EXIT = "Назад"
    CLEAR = "Убрать категорию из всех товаров"
    FULL = "Убрать категорию из всех товаров и удалить"

    def __str__(self) -> str:
        return self.value


class CategoryDeleterViewer(Viewer):
    """CLI-фронтенд для удаления категорий"""

    def __read_action(self):
        message = "Выберите действие"
        choices = list(Action)
        action = super().select(message=message, choices=choices)
        return action

    def __select_categories(self) -> List[Category]:
        message = "Выберите категории для удаления"
        categories: List[Category] = self.select_category(
            message=message,
            multiselect=True,
        )
        return categories

    def attach(self):
        """Присоединение CLI-фронтенда к терминалу"""
        categories = self.__select_categories()
        action = self.__read_action()

        if action == Action.CLEAR:
            self.database.reset_categories(categories)
        elif action == Action.FULL:
            self.database.delete_categories(categories)
