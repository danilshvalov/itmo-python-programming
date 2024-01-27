from enum import Enum


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def is_same(self, other):
        return self.row == other.row and self.col == other.col

    def __str__(self):
        return f"({self.row}, {self.col})"


class PlayerColor(Enum):
    BLACK = "black"
    WHITE = "white"
