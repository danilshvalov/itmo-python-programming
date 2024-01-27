"""Модуль с CLI-фронтендом, реализующим интерфейс поиска расходов"""

from typing import List
from enum import Enum

from finacsys.database import Database, ExpenseFinder
from finacsys.filters import (
    DateFilter,
    TimeFilter,
    CategoriesFilter,
    FilterKind,
)
from finacsys.models import Expense

from ..viewer import Viewer


class Action(Enum):
    """Действия, предлагаемые пользователю для поиска"""

    STOP_SEARCHING = "Завершить поиск"
    FIND_BY_TEXT = "Поиск текстом"
    ADD_FILTERS = "Добавить фильтры"

    def __str__(self) -> str:
        return self.value


class ExpenseFinderViewer(Viewer):
    """Класс реализует CLI-фронтенд для фильтрации различных статей расходов"""

    def __init__(self, database: Database):
        super().__init__(database)
        self.finder = ExpenseFinder(database)

    def __find_by_text(self) -> List[Expense]:
        message = "Выберите позиции"
        choices = self.finder.filtered_expenses

        expenses = super().multiselect(message=message, choices=choices)

        self.finder.filtered_expenses = expenses
        return expenses

    def __read_time_filter(self) -> TimeFilter:
        message = "Выберите тип фильтра"
        choices = list(TimeFilter)

        time_filter = super().select(message=message, choices=choices)
        return time_filter

    def __set_time_filter(self):
        filter_type = self.__read_time_filter()
        date = super().read_time()
        self.finder.set_time_filter(filter_type, date)

    def __read_date_filter(self) -> DateFilter:
        message = "Выберите тип фильтра"
        choices = list(DateFilter)

        time_filter = super().select(message=message, choices=choices)
        return time_filter

    def __set_date_filter(self):
        filter_type = self.__read_date_filter()
        date = super().read_date()
        self.finder.set_date_filter(filter_type, date)

    def __read_category_filter(self) -> CategoriesFilter:
        message = "Выберите тип фильтра"
        choices = list(CategoriesFilter)

        category_filter = super().select(message=message, choices=choices)
        return category_filter

    def __set_category_filter(self):
        message = "Выберите категории"
        categories = self.select_category(message=message, multiselect=True)
        filter_type = self.__read_category_filter()

        if filter_type == CategoriesFilter.EXCLUDE_CATEGORIES:
            return self.finder.exclude_categories(categories)
        if filter_type == CategoriesFilter.ONLY_INCLUDED:
            return self.finder.only_included_categories(categories)

        raise NotImplementedError()

    def __stop_searching(self) -> List[Expense]:
        return self.finder.release_expenses()

    def __gen_actions(self) -> List[Action]:
        result = [Action.STOP_SEARCHING]
        if self.finder.has_avaliable_filters():
            result.append(Action.ADD_FILTERS)
        if not self.finder.empty():
            result.append(Action.FIND_BY_TEXT)

        return result

    def __read_action(self) -> Action:
        message = "Выберите действие"
        choices = self.__gen_actions()

        action = super().select(message=message, choices=choices)
        return action

    def __read_filter(self) -> FilterKind:
        message = "Выберите фильтр"
        choices = self.finder.get_avaliable_filters()
        selected_filter = super().select(message=message, choices=choices)
        return selected_filter

    def __add_filters(self):
        filter_kind = self.__read_filter()

        if filter_kind == FilterKind.FILTER_BY_DATE:
            return self.__set_date_filter()
        if filter_kind == FilterKind.FILTER_BY_TIME:
            return self.__set_time_filter()
        if filter_kind == FilterKind.FILTER_BY_CATEGORY:
            return self.__set_category_filter()

        raise NotImplementedError()

    def attach(self) -> List[Expense]:
        """Присоединение CLI-фронтенда к консоли"""

        self.finder.filtered_expenses = self.database.get_expenses_list()

        while True:
            action = self.__read_action()

            if len(self.finder.filtered_expenses) == 0:
                return self.__stop_searching()

            if action == Action.ADD_FILTERS:
                self.__add_filters()
            elif action == Action.FIND_BY_TEXT:
                self.__find_by_text()
            elif action == Action.STOP_SEARCHING:
                return self.__stop_searching()
