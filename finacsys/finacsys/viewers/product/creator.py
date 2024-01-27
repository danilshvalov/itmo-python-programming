"""Модуль с CLI-фронтендом для создания товаров"""

from typing import List
from InquirerPy import inquirer

from finacsys.models import Category, Product

from ..viewer import Viewer


class ProductCreatorViewer(Viewer):
    """Класс, реализующий CLI-фронтенд по созданию товаров"""

    def __read_categories(self):
        message = "Выберите категории"
        categories = super().select_category(message=message, multiselect=True)
        return categories

    def __ask_categories_if_exists(self) -> List[Category]:
        if len(self.database.get_categories_list()) == 0:
            return []

        choose_categories = inquirer.confirm(
            message="Вы хотите установить категории этому товару?"
        ).execute()

        if not choose_categories:
            return []

        categories = self.__read_categories()
        return categories

    def attach(self):
        """Присоединение CLI-фронтенда к консоли"""
        name = super().read_name()
        price = super().read_price()
        categories: List[Category] = self.__ask_categories_if_exists()

        product = Product(name, price, categories)
        self.database.add_product(product)
