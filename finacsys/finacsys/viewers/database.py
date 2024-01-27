"""Модуль, включающий в себя реализацию CLI-фронтенда базы данных"""
from enum import Enum
from typing import List

from finacsys.database import Database

from .viewer import Viewer
from .product import ProductViewer
from .category import CategoryViewer
from .expense import ExpenseViewer


class Command(Enum):
    """Команды, доступные пользователю для взаимодействия с БД"""

    EXIT = "Выйти"
    PRODUCTS = "Товары"
    CATEGORIES = "Категории"
    EXPENSES = "Статьи расходов"

    def __str__(self) -> str:
        return self.value


class DatabaseViewer(Viewer):
    """Класс, реализующий CLI-фронтенд базы данных"""

    def __init__(self, db: Database):
        super().__init__(db)
        self.product_viewer = ProductViewer(db)
        self.category_viewer = CategoryViewer(db)
        self.expenses_viewer = ExpenseViewer(db)

    def __gen_commands(self) -> List[Command]:
        commands = [Command.EXIT, Command.PRODUCTS, Command.CATEGORIES]

        if len(self.database.products) > 0:
            commands.append(Command.EXPENSES)

        return commands

    def __read_command(self):
        message = "Выберите действие:"
        choices = self.__gen_commands()

        action = super().select(message=message, choices=choices)
        return action

    def attach(self):
        """Присоединение CLI-фронтенда к консоли"""
        while True:
            command = self.__read_command()

            if command == Command.EXIT:
                break

            if command == Command.PRODUCTS:
                self.product_viewer.attach()
            elif command == Command.CATEGORIES:
                self.category_viewer.attach()
            elif command == Command.EXPENSES:
                self.expenses_viewer.attach()
