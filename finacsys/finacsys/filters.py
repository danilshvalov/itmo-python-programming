"""Модуль, содержащий различные виды фильтров"""

from enum import Enum
from typing import Callable, Any
import datetime as dt


class FilterKind(Enum):
    """Тип фильтра"""

    FILTER_BY_DATE = "Отфильтровать по дате"
    FILTER_BY_TIME = "Отфильтровать по времени"
    FILTER_BY_CATEGORY = "Отфильтровать по категориям"

    def __str__(self) -> str:
        return self.value


class DateFilter(Enum):
    """Типы фильтрации дат"""

    LT = "Раньше указанной даты"
    LE = "Раньше или равно указанной дате"
    EQ = "Равно указанной дате"
    GE = "Позже или равно указанной дате"
    GT = "Позже указанной даты"

    def __str__(self) -> str:
        return self.value


def make_date_cmp(
    filter_type: DateFilter, date: dt.date
) -> Callable[[Any], bool]:
    """Создание компаратора в соответствии с типом фильтра"""

    if filter_type == DateFilter.LT:
        return lambda x: x.get_date() < date
    if filter_type == DateFilter.LE:
        return lambda x: x.get_date() <= date
    if filter_type == DateFilter.EQ:
        return lambda x: x.get_date() == date
    if filter_type == DateFilter.GE:
        return lambda x: x.get_date() >= date
    if filter_type == DateFilter.GT:
        return lambda x: x.get_date() > date
    raise NotImplementedError()


class TimeFilter(Enum):
    """Типы фильтрации времени"""

    LT = "Раньше указанного времени"
    LE = "Раньше или равно указанному времени"
    EQ = "Равно указанному времени"
    GE = "Позже или равно указанному времени"
    GT = "Позже указанного времени"

    def __str__(self) -> str:
        return self.value


def make_time_cmp(
    filter_type: TimeFilter, time: dt.time
) -> Callable[[Any], bool]:
    """Создание компаратора в соответствии с типом фильтра"""

    if filter_type == TimeFilter.LT:
        return lambda x: x.get_time() < time
    if filter_type == TimeFilter.LE:
        return lambda x: x.get_time() <= time
    if filter_type == TimeFilter.EQ:
        return lambda x: x.get_time() == time
    if filter_type == TimeFilter.GE:
        return lambda x: x.get_time() >= time
    if filter_type == TimeFilter.GT:
        return lambda x: x.get_time() > time
    raise NotImplementedError()


class CategoriesFilter(Enum):
    """Типы фильтрации категорий"""

    EXCLUDE_CATEGORIES = "Исключить выбранные категории"
    ONLY_INCLUDED = "Оставить только выбранные категории"

    def __str__(self) -> str:
        return self.value
