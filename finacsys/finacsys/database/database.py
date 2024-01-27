"""Модуль, содержащий базу данных приложения"""
from typing import List
from uuid import UUID

from finacsys.models import Product, Category, Expense

from .tables import ProductTable, ExpenseTable, Table

CategoryTable = Table


class Database:
    """
    База данных приложения. Включает в себя таблицу категорий, товаров и
    расходов
    """

    def __init__(self):
        self.expenses = ExpenseTable()
        self.products = ProductTable()
        self.categories = CategoryTable()

    def add_product(self, product: Product) -> UUID:
        """Добавление товара в базу данных"""
        self.products[product.get_id()] = product
        return product.get_id()

    def add_category(self, category: Category) -> UUID:
        """Добавление категории в базу данных"""
        self.categories[category.get_id()] = category
        return category.get_id()

    def add_expense(self, product_item: Expense) -> UUID:
        """Добавление статьи расхода в базу данных"""
        self.expenses[product_item.get_id()] = product_item
        return product_item.get_id()

    def get_products_list(self) -> List[Product]:
        """Получение списка товаров"""
        return list(self.products.values())

    def get_categories_list(self) -> List[Category]:
        """Получение списка категорий"""
        return list(self.categories.values())

    def get_expenses_list(self) -> List[Expense]:
        """Получение списка расходов"""
        return list(self.expenses.values())

    def reset_category(self, category: Category):
        """Удалить категорию из всех товаров"""
        for product in self.products.values():
            product.get_categories().discard(category)

    def reset_categories(self, categories: list[Category]):
        """Удалить список категорий из всех товаров"""
        for category in categories:
            self.reset_category(category)

    def delete_category(self, category: Category):
        """Удалить одну категорию"""
        self.reset_category(category)
        self.categories.pop(category.get_id())

    def delete_categories(self, categories: list[Category]):
        """Удалить список категорий"""
        for category in categories:
            self.delete_category(category)
