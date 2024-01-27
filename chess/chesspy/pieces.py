from abc import ABC, abstractmethod

from .types import Position, PlayerColor


class ChessPiece(ABC):
    def __init__(self, color: PlayerColor, icon):
        super().__init__()
        self.__icon = icon
        self.__color = color

    def is_same_color(self, color):
        return self.__color == color

    def get_color(self):
        return self.__color

    def get_icon(self):
        return self.__icon

    @abstractmethod
    def check_direction(self, before: Position, after: Position):
        pass

    def can_move(self, before: Position, after: Position):
        return self.check_direction(before, after)

    def can_kill(self, before: Position, after: Position):
        return self.check_direction(before, after)


class Queen(ChessPiece):
    def check_direction(self, before: Position, after: Position):
        return (
            abs(after.row - before.row) == abs(after.col - before.col)
            or after.row == before.row
            and after.col != before.col
            or after.col == before.col
            and after.row != before.row
        )


class King(ChessPiece):
    def check_direction(self, before: Position, after: Position):
        return abs(after.row - before.row) == 1 or abs(after.col - before.col) == 1


class Bishop(ChessPiece):
    def check_direction(self, before: Position, after: Position):
        return abs(after.row - before.row) == abs(after.col - before.col)


class Knight(ChessPiece):
    def check_direction(self, before: Position, after: Position):
        return (
            abs(after.row - before.row) == 2 and abs(after.col - before.col) == 1
        ) or (abs(after.col - before.col) == 2 and abs(after.row - before.row) == 1)


class Rook(ChessPiece):
    def check_direction(self, before, after):
        return (
            before.row == after.row
            and before.col != after.col
            or before.col == after.col
            and before.row != after.row
        )


class Pawn(ChessPiece):
    def __init__(self, color: PlayerColor, icon):
        super().__init__(color=color, icon=icon)
        self.__first_step = True

    def check_direction(self, before: Position, after: Position):
        return before.row > after.row

    def can_move(self, before: Position, after: Position):
        if not self.check_direction(before, after):
            return False

        if (
            not (self.__first_step and 1 <= abs(after.row - before.row) <= 2)
            and not abs(after.row - before.row) == 1
            or after.col != before.col
        ):
            return False

        self.__first_step = False
        return True

    def can_kill(self, before: Position, after: Position):
        if not self.check_direction(before, after):
            return False

        return abs(after.row - before.row) == 1 and abs(after.col - before.col) == 1
