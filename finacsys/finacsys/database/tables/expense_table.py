"""Модуль, включающий в себя реализацию таблицы расходов"""
from typing import List

from finacsys.models import Expense, Category, Product

from .table import Table


class ExpenseTable(Table[Expense]):
    """Класс, представляющий таблицу расходов"""

    def pop_by_category(self, category: Category) -> List[Expense]:
        """Удаление статей расходов, принадлежащих к переданной категории"""
        removed = super().pop_by(
            lambda expense: category in expense.get_categories(),
        )
        return removed

    def pop_by_product(self, product: Product) -> List[Expense]:
        """Удаление статей расходов, основанных на переданном товаре"""
        removed = super().pop_by(
            lambda expense: product == expense.get_product_id(),
        )
        return removed
