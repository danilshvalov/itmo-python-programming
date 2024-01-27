"""Модуль, содержащий класс для поиска и фильтрации товаров"""
from typing import List

from finacsys.models import Category
from finacsys.filters import FilterKind
from finacsys.database import Database


class ProductFinder:
    """Класс для поиска и фильтрации товаров по категориям"""

    def __init__(self, database: Database):
        self.database = database
        self.filtered_products = self.database.get_products_list()

    def only_included_categories(self, categories: List[Category]):
        """
        Удаляет из поиска те товары, которые не принадлежат хотя бы к одной
        категории из переданного списка категорий
        """
        result = []

        for product in self.filtered_products:
            is_contains_category = False
            for category in product.get_categories():
                is_contains_category = category in categories
                if is_contains_category:
                    break
            if is_contains_category:
                result.append(product)

        self.filtered_products = result

    def exclude_categories(self, categories: List[Category]):
        """
        Удаляет из поиска те товары, которые принадлежат к хотя бы одной
        категории из переданного списка категорий
        """
        result = []

        for product in self.filtered_products:
            is_contains_category = False
            for category in product.get_categories():
                is_contains_category = category in categories
                if is_contains_category:
                    break
            if not is_contains_category:
                result.append(product)

        self.filtered_products = result

    def get_avaliable_filters(self):
        """Получение списка доступных фильтров"""
        result = []

        if len(self.database.categories) > 0:
            result.append(FilterKind.FILTER_BY_CATEGORY)

        return result

    def has_avaliable_filters(self) -> bool:
        """Проверка на наличие доступных фильтров"""
        return len(self.get_avaliable_filters()) != 0

    def empty(self) -> bool:
        """Проверка отфильтрованного списка товаров на пустоту"""
        return len(self.filtered_products) == 0

    def release_products(self):
        """
        Возвращает отфильтрованный список, после чего удерживаемый список
        синхронизируется с данными БД
        """
        products = self.filtered_products
        self.filtered_products = self.database.get_products_list()
        return products
