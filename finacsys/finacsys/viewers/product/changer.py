"""Модуль, содержащий CLI-фронтенд для изменения товаров"""
from typing import List
from enum import Enum

from finacsys.models import Product

from ..viewer import Viewer


class Action(Enum):
    """Действия, доступные пользователю для изменения товаров"""

    EXIT = "Назад"
    CHANGE_NAME = "Изменить названия товаров"
    CHANGE_PRICE = "Изменить цену товаров"
    ADD_CATEGORIES = "Добавить категории"
    REMOVE_CATEGORIES = "Убрать категории"

    def __str__(self) -> str:
        return self.value


class ProductChangerViewer(Viewer):
    """Класс, представляющий CLI-фронтенд для изменения товаров"""

    def __change_name(self, products: List[Product]):
        new_name = super().read_name()
        for product in products:
            product.set_name(new_name)

    def __change_price(self, products: List[Product]):
        new_price = super().read_price()
        for product in products:
            product.set_price(new_price)

    def __add_categories(self, products: List[Product]):
        message = "Выберите категории для добавления в товары"
        categories = super().select_category(message=message, multiselect=True)

        for product in products:
            product.add_categories(categories)

    def __remove_categories(self, products: List[Product]):
        message = "Выберите категории для удаления из товаров"
        categories = super().select_category(message=message, multiselect=True)

        for product in products:
            product.remove_categories(categories)

    def __read_action(self) -> Action:
        choices = list(Action)

        action = super().select(message="Выберите действие", choices=choices)

        return action

    def __select_products(self):
        message = "Выберите товары для изменения"
        products = self.select_product(message=message, multiselect=True)
        return products

    def attach(self):
        """Присоединение CLI-фронтенда к консоли"""
        products = self.__select_products()
        while True:
            action = self.__read_action()

            if action == Action.EXIT:
                break

            if action == Action.CHANGE_NAME:
                self.__change_name(products)
            elif action == Action.CHANGE_PRICE:
                self.__change_price(products)
            elif action == Action.ADD_CATEGORIES:
                self.__add_categories(products)
            elif action == Action.REMOVE_CATEGORIES:
                self.__remove_categories(products)
