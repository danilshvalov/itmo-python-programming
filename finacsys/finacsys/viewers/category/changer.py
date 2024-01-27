"""Модуль с CLI-фронтендом для изменения категорий"""
from typing import List
from enum import Enum

from finacsys.models import Category

from ..viewer import Viewer


class Action(Enum):
    """Действия, доступные пользователю для изменения категорий"""

    EXIT = "Назад"
    CHANGE_NAME = "Изменить название категории"

    def __str__(self) -> str:
        return self.value


class CategoryChangerViewer(Viewer):
    """Класс, реализующий CLI-фронтенд для изменения категорий"""

    def __read_change_action(self) -> Action:
        message = "Выберите действие"
        choices = list(Action)
        action = super().select(message=message, choices=choices)
        return action

    def __select_categories(self):
        message = "Выберите категории для изменения"
        categories = self.select_category(message=message, multiselect=True)
        return categories

    def __change_names(self, categories: List[Category]):
        name = super().read_name()
        for category in categories:
            category.set_name(name)

    def attach(self):
        """Присоединение CLI-фронтенда к консоли"""
        categories = self.__select_categories()
        action = self.__read_change_action()

        if action == Action.CHANGE_NAME:
            self.__change_names(categories)
