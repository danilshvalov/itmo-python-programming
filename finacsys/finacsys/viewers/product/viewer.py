"""Модуль с CLI-фронтендом для взаимодействия с товарами"""

from enum import Enum
from typing import List
from InquirerPy import inquirer

from finacsys.database import Database
from finacsys.models import Product
from finacsys.viewers.utils import confirm_sort
from finacsys.viewers.fs import write_to_file, confirm_write_to_file

from ..viewer import Viewer
from .creator import ProductCreatorViewer
from .finder import ProductFinderViewer
from .changer import ProductChangerViewer
from .sorter import ProductSorterViewer
from .utils import make_table


class Command(Enum):
    """Доступные пользователю действия над товарами"""

    CREATE = "Создать товар"
    VIEW_ALL = "Показать все товары"
    FIND = "Найти товары"
    CHANGE = "Изменить товары"
    DELETE = "Удалить товары"
    EXIT = "Назад"

    def __str__(self) -> str:
        return self.value


class ProductViewer(Viewer):
    """CLI-фронтенд для взаимодействия с товарами"""

    def __init__(self, database: Database):
        super().__init__(database)
        self.__creator = ProductCreatorViewer(database)
        self.__finder = ProductFinderViewer(database)
        self.__changer = ProductChangerViewer(database)
        self.__sorter = ProductSorterViewer(database)

    def __gen_commands(self):
        commands = [Command.EXIT, Command.CREATE]

        if len(self.database.products) > 0:
            commands.append(Command.VIEW_ALL)
            commands.append(Command.FIND)
            commands.append(Command.CHANGE)
            commands.append(Command.DELETE)

        return commands

    def __read_command(self) -> Command:
        message = "Выберите действие"
        choices = self.__gen_commands()
        command = super().select(message=message, choices=choices)
        return command

    def __view_all(self):
        rows = self.database.get_products_list()
        self.__print_products(rows)

    def __find_products(self):
        products = self.__finder.attach()
        self.__print_products(products)

    def __print_product_list(self, products: List[Product]):
        if confirm_sort():
            products = self.__sorter.attach(products)

        table = make_table(products)
        if confirm_write_to_file():
            write_to_file(table)
        print(table)

    def __print_products(self, products: List[Product]):
        if len(products) == 0:
            print("Ничего не удалось найти")
        else:
            self.__print_product_list(products)

    def __delete_products(self):
        print("Выберите товары для удаления")
        products = self.__finder.attach()

        if len(products) == 0:
            print("Ничего не нашлось")

        message = (
            "Вы действительно хотите удалить товаров в количестве "
            f"{len(products)} шт?"
        )
        confirm = inquirer.confirm(message).execute()

        if confirm:
            for product in products:
                self.database.products.pop(product.get_id())

    def attach(self):
        """Присоединение CLI-фронтенда к терминалу"""
        while True:
            command = self.__read_command()
            if command == Command.EXIT:
                break

            if command == Command.VIEW_ALL:
                self.__view_all()
            if command == Command.CREATE:
                self.__creator.attach()
            if command == Command.FIND:
                self.__find_products()
            if command == Command.CHANGE:
                self.__changer.attach()
            if command == Command.DELETE:
                self.__delete_products()
