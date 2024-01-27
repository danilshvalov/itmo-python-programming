"""Модуль, содержащий класс для поиска и фильтрации расходов"""
from typing import List
import datetime as dt

from finacsys.models import Category
from finacsys.filters import (
    FilterKind,
    make_date_cmp,
    make_time_cmp,
    TimeFilter,
    DateFilter,
)
from finacsys.database import Database


class ExpenseFinder:
    """
    Класс предоставляет поиск и фильтрацию списка расходов по категориям,
    дате и времени
    """

    def __init__(self, database: Database):
        self.database = database
        self.filtered_expenses = self.database.get_expenses_list()

    def only_included_categories(self, categories: List[Category]):
        """
        Удаляет из поиска те статьи расхода, которые не принадлежат к хотя бы
        одной категории из переданного списка категорий
        """
        result = []

        for expense in self.filtered_expenses:
            is_contains_category = False
            for category in expense.get_categories():
                is_contains_category = category in categories
                if is_contains_category:
                    break
            if is_contains_category:
                result.append(expense)

        self.filtered_expenses = result

    def exclude_categories(self, categories: List[Category]):
        """
        Удаляет из поиска те статьи расхода, которые принадлежат к хотя бы
        одной категории из переданного списка категорий
        """
        result = []

        for expense in self.filtered_expenses:
            is_contains_category = False
            for category in expense.get_categories():
                is_contains_category = category in categories
                if is_contains_category:
                    break
            if not is_contains_category:
                result.append(expense)

        self.filtered_expenses = result

    def set_date_filter(self, filter_type: DateFilter, date: dt.date):
        """Отфильтровать список по дате. См. DateFilter"""
        cmp = make_date_cmp(filter_type, date)
        self.filtered_expenses = list(filter(cmp, self.filtered_expenses))

    def set_time_filter(self, filter_type: TimeFilter, time: dt.time):
        """Отфильтровать список по времени. См. TimeFilter"""
        cmp = make_time_cmp(filter_type, time)
        self.filtered_expenses = list(filter(cmp, self.filtered_expenses))

    def get_avaliable_filters(self) -> List[FilterKind]:
        """Получение списка доступных фильтров"""
        result = [FilterKind.FILTER_BY_DATE, FilterKind.FILTER_BY_TIME]

        if len(self.database.categories) > 0:
            result.append(FilterKind.FILTER_BY_CATEGORY)

        return result

    def has_avaliable_filters(self) -> bool:
        return len(self.get_avaliable_filters()) > 0

    def empty(self) -> bool:
        """Проверка отфильтрованного списка расходов на пустоту"""
        return len(self.filtered_expenses) == 0

    def release_expenses(self):
        """
        Возвращает отфильтрованный список, после чего удерживаемый список
        синхронизируется с данными БД
        """
        expenses = self.filtered_expenses
        self.filtered_expenses = self.database.get_expenses_list()
        return expenses
