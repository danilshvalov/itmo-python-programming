"""Модуль с утилитами"""

from typing import List

from finacsys.models import Product
from finacsys.utils import make_str_table


def __product_to_table_row(product: Product) -> List[str]:
    ident = str(product.get_id())
    name = product.get_name()
    price = str(product.get_price())
    categories = "\n".join(map(str, product.get_categories()))
    return [ident, name, price, categories]


def make_table(products: List[Product]) -> str:
    """Создание таблицы товаров

    Args:
        products (List[Product]): список товаров, которые будут включены
        в таблицу

    Returns:
        str: строковое представление таблицы
    """
    header = [["ID", "Название", "Цена", "Категории"]]
    rows = [__product_to_table_row(p) for p in products]
    table = make_str_table(header, rows)
    return table
