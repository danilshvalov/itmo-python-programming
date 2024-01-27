"""
Модуль, включающий в себя основные компоненты CLI-фронтенда
для взаимодействия с категориям
"""

from enum import Enum
from typing import List

from finacsys.database import Database
from finacsys.models import Category
from finacsys.viewers.utils import confirm_sort
from finacsys.viewers.fs import write_to_file, confirm_write_to_file

from ..viewer import Viewer
from .changer import CategoryChangerViewer
from .deleter import CategoryDeleterViewer
from .sorter import CategorySorterViewer
from .utils import make_table


class Command(Enum):
    """Комманды для взаимодействия с категориями"""

    CREATE = "Создать категорию"
    VIEW_ALL = "Показать все категории"
    CHANGE = "Изменить категорию"
    DELETE = "Удалить категорию"
    EXIT = "Назад"

    def __str__(self) -> str:
        return self.value


class CategoryViewer(Viewer):
    """Класс, реализующий основной функционал CLI-фронтенда для категорий"""

    def __init__(self, database: Database):
        super().__init__(database)
        self.__changer = CategoryChangerViewer(database)
        self.__deleter = CategoryDeleterViewer(database)
        self.__sorter = CategorySorterViewer(database)

    def __gen_commands(self) -> List[Command]:
        commands = [Command.EXIT, Command.CREATE]
        if len(self.database.categories) > 0:
            commands.append(Command.VIEW_ALL)
            commands.append(Command.CHANGE)
            commands.append(Command.DELETE)
        return commands

    def __read_command(self) -> Command:
        message = "Выберите действие"
        choices = self.__gen_commands()
        command = super().select(message=message, choices=choices)
        return command

    def __create_category(self):
        name = super().read_name()
        category = Category(name)
        self.database.add_category(category)

    def __print_category_list(self, categories: List[Category]):
        if confirm_sort():
            categories = self.__sorter.attach(categories)

        table = make_table(categories)
        if confirm_write_to_file():
            write_to_file(table)
        print(table)

    def __print_categories(self, categories: List[Category]):
        if len(categories) == 0:
            print("Ничего не удалось найти")
        else:
            self.__print_category_list(categories)

    def __view_all(self):
        categories = self.database.get_categories_list()
        self.__print_categories(categories)

    def attach(self):
        """Присоединение CLI-фронтенда к консоли"""
        while True:
            command = self.__read_command()

            if command == Command.EXIT:
                break

            if command == Command.CREATE:
                self.__create_category()
            elif command == Command.VIEW_ALL:
                self.__view_all()
            elif command == Command.CHANGE:
                self.__changer.attach()
            elif command == Command.DELETE:
                self.__deleter.attach()
