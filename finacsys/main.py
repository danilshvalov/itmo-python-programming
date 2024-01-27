"""Основной модуль, запускающий приложение"""
from finacsys.viewers import DatabaseViewer
from finacsys.database import Database


def main():
    """Функция запуска приложения"""
    database = Database()
    database_viewer = DatabaseViewer(database)
    database_viewer.attach()


if __name__ == "__main__":
    main()
