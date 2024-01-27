"""Модуль, содержащий в себе реализацию таблицы товаров"""
from typing import List

from finacsys.models import Product, Category

from .table import Table


class ProductTable(Table[Product]):
    """Класс, представляющий таблицу товаров"""

    def pop_by_category(self, category: Category) -> List[Product]:
        """Удаление товаров, принадлежащих к переданной категории"""
        removed = self.pop_by(
            lambda product: category in product.get_categories(),
        )
        return removed
