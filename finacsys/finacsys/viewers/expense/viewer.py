"""Модуль, реализующий основную функциональность CLI-фронтенда"""
from typing import List
from enum import Enum
from InquirerPy import inquirer

from finacsys.database import Database
from finacsys.models import Expense
from finacsys.viewers.utils import confirm_sort
from finacsys.viewers.fs import write_to_file, confirm_write_to_file

from ..viewer import Viewer
from .finder import ExpenseFinderViewer
from .changer import ExpenseChangerViewer
from .sorter import ExpenseSorterViewer
from .utils import make_table


class Command(Enum):
    """Команды, доступные пользователю для взаимодействия с списком расходов"""

    EXIT = "Назад"
    CREATE = "Добавить новую статью расхода"
    VIEW_ALL = "Показать все статьи расходов"
    FIND = "Найти статьи расходов"
    CHANGE = "Изменить статьи расхода"
    DELETE = "Удалить статьи расхода"

    def __str__(self) -> str:
        return self.value


class ExpenseViewer(Viewer):
    """Класс, реализующий основной CLI-фронтенд"""

    def __init__(self, database: Database):
        super().__init__(database)
        self.__changer = ExpenseChangerViewer(database)
        self.__finder = ExpenseFinderViewer(database)
        self.__sorter = ExpenseSorterViewer(database)

    def __create_expense(self):
        product = self.select_product(message="Выберите товар")
        count = super().read_count()
        datetime = super().read_datetime()
        expense = Expense(product, count, datetime)
        self.database.add_expense(expense)

    def __gen_commands(self) -> List[Command]:
        commands = [Command.EXIT, Command.CREATE]

        if len(self.database.expenses) > 0:
            commands.append(Command.VIEW_ALL)
            commands.append(Command.FIND)
            commands.append(Command.CHANGE)
            commands.append(Command.DELETE)

        return commands

    def __read_command(self):
        message = "Выберите действие"
        choices = self.__gen_commands()

        command: Command = super().select(message=message, choices=choices)

        return command

    def __change_expenses(self):
        expenses = self.__finder.attach()

        if len(expenses) > 0:
            self.__changer.attach(expenses)

    def __delete_expenses(self):
        print("Выберите статьи расхода для удаления")
        expenses = self.__finder.attach()

        message = (
            "Вы действительно хотите удалить статьи расхода в"
            + f"количестве {len(expenses)} шт.?"
        )
        confirm = inquirer.confirm(message).execute()

        if confirm:
            for expense in expenses:
                self.database.expenses.pop(expense.get_id())

    def __view_all(self):
        expenses = self.database.get_expenses_list()
        self.__print_expenses(expenses)

    def __print_expenses(self, expenses: List[Expense]):
        if confirm_sort():
            expenses = self.__sorter.attach(expenses)

        table = make_table(expenses)
        if confirm_write_to_file():
            write_to_file(table)
        print(table)

    def __find_expenses(self):
        expenses = self.__finder.attach()

        if len(expenses) == 0:
            print("Ничего не удалось найти")
        else:
            self.__print_expenses(expenses)

    def __dispatch_command(self, command: Command):
        if command == Command.CREATE:
            self.__create_expense()
        elif command == Command.VIEW_ALL:
            self.__view_all()
        elif command == Command.FIND:
            self.__find_expenses()
        elif command == Command.CHANGE:
            self.__change_expenses()
        elif command == Command.DELETE:
            self.__delete_expenses()
        else:
            raise NotImplementedError()

    def attach(self):
        """Присоединение CLI-фронтенда к консоли"""
        while True:
            command = self.__read_command()

            if command == Command.EXIT:
                break

            self.__dispatch_command(command)
