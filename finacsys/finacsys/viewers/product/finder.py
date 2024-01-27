"""Модуль с CLI-фронтедом, представляющим поиск по товарам"""
from typing import List
from enum import Enum

from finacsys.database import Database, ProductFinder
from finacsys.filters import CategoriesFilter, FilterKind
from finacsys.models import Product

from ..viewer import Viewer


class Action(Enum):
    """Доступные для поиска команды"""

    STOP_SEARCHING = "Завершить поиск"
    FIND_BY_TEXT = "Поиск текстом"
    ADD_FILTERS = "Добавить фильтры"

    def __str__(self) -> str:
        return self.value


class ProductFinderViewer(Viewer):
    """CLI-фронтенд для поиска товаров"""

    def __init__(self, database: Database):
        super().__init__(database)
        self.finder = ProductFinder(database)

    def __find_by_text(self) -> List[Product]:
        message = "Выберите позиции"
        choices = self.finder.filtered_products

        products = super().multiselect(message=message, choices=choices)

        self.finder.filtered_products = products

        return products

    def __read_category_filter(self) -> CategoriesFilter:
        message = "Выберите тип фильтра"
        choices = [
            CategoriesFilter.ONLY_INCLUDED,
            CategoriesFilter.EXCLUDE_CATEGORIES,
        ]

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

    def __gen_actions(self) -> List[Action]:
        actions = [Action.STOP_SEARCHING]
        if not self.finder.empty():
            actions.append(Action.FIND_BY_TEXT)
        if self.finder.has_avaliable_filters():
            actions.append(Action.ADD_FILTERS)
        return actions

    def __stop_searching(self):
        result = self.finder.release_products()
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

        if filter_kind == FilterKind.FILTER_BY_CATEGORY:
            return self.__set_category_filter()

        raise NotImplementedError()

    def attach(self):
        """Присоединение CLI-фронтенда к терминалу"""
        self.finder.filtered_products = self.database.get_products_list()

        while True:
            action = self.__read_action()

            if action == Action.STOP_SEARCHING:
                return self.__stop_searching()

            if action == Action.ADD_FILTERS:
                self.__add_filters()
            elif action == Action.FIND_BY_TEXT:
                self.__find_by_text()
