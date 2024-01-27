import tkinter as tk

from .types import PlayerColor, Position
from .pieces import Pawn, Bishop, Queen, King, Rook, Knight, ChessPiece
from .utils import empty_matrix


class IconHolder:
    def __init__(self):
        self.queen_white = self.load_icon("images/queen_white.png")
        self.queen_black = self.load_icon("images/queen_black.png")
        self.king_white = self.load_icon("images/king_white.png")
        self.king_black = self.load_icon("images/king_black.png")
        self.bishop_white = self.load_icon("images/bishop_white.png")
        self.bishop_black = self.load_icon("images/bishop_black.png")
        self.knight_white = self.load_icon("images/knight_white.png")
        self.knight_black = self.load_icon("images/knight_black.png")
        self.pawn_white = self.load_icon("images/pawn_white.png")
        self.pawn_black = self.load_icon("images/pawn_black.png")
        self.rook_white = self.load_icon("images/rook_white.png")
        self.rook_black = self.load_icon("images/rook_black.png")

    def load_icon(self, filename):
        image = tk.PhotoImage(file=filename)
        image = image.subsample(3, 3)
        return image


class Board(tk.Frame):
    def __init__(self, root, cell_count, cell_size):
        super().__init__(root)

        self.__stroke_number = 0

        self.cell_count = cell_count
        self.cell_size = cell_size
        self.icons = IconHolder()

        self.__board = empty_matrix(self.cell_count)
        self.fill_field()

        self.canvas = tk.Canvas(self)
        self.click_bind = self.canvas.bind("<Button-1>", self.on_click)
        self.click_poses = []
        self.init_ui()

    def on_click(self, event):
        self.click_poses.append(self.get_pos(event.x, event.y))

        if len(self.click_poses) >= 2:
            before, after = self.click_poses[-2:]
            self.move(before, after)
            self.click_poses.clear()
            self.draw()

    def get_pos(self, x, y):
        row = y // self.cell_size
        col = x // self.cell_size
        return Position(row, col)

    def fill_field(self):
        self.__board[0] = [
            Rook(PlayerColor.BLACK, self.icons.rook_black),
            Knight(PlayerColor.BLACK, self.icons.knight_black),
            Bishop(PlayerColor.BLACK, self.icons.bishop_black),
            King(PlayerColor.BLACK, self.icons.king_black),
            Queen(PlayerColor.BLACK, self.icons.queen_black),
            Bishop(PlayerColor.BLACK, self.icons.bishop_black),
            Knight(PlayerColor.BLACK, self.icons.knight_black),
            Rook(PlayerColor.BLACK, self.icons.rook_black),
        ]
        self.__board[1] = [
            Pawn(PlayerColor.BLACK, self.icons.pawn_black)
            for _ in range(self.cell_count)
        ]

        self.__board[-1] = [
            Rook(PlayerColor.WHITE, self.icons.rook_white),
            Knight(PlayerColor.WHITE, self.icons.knight_white),
            Bishop(PlayerColor.WHITE, self.icons.bishop_white),
            King(PlayerColor.WHITE, self.icons.king_white),
            Queen(PlayerColor.WHITE, self.icons.queen_white),
            Bishop(PlayerColor.WHITE, self.icons.bishop_white),
            Knight(PlayerColor.WHITE, self.icons.knight_white),
            Rook(PlayerColor.WHITE, self.icons.rook_white),
        ]
        self.__board[-2] = [
            Pawn(PlayerColor.WHITE, self.icons.pawn_white)
            for _ in range(self.cell_count)
        ]

    def draw(self):
        self.canvas.delete("all")
        self.canvas.pack()

        rows = cols = self.cell_count
        size = self.cell_size

        for row in range(rows):
            for col in range(cols):
                color = "#808ba0" if (row + col) % 2 else "#dbdbdd"
                self.canvas.create_rectangle(
                    col * size,
                    row * size,
                    (col + 1) * size,
                    (row + 1) * size,
                    fill=color,
                )

        offset = size // 2

        for row in range(rows):
            for col in range(cols):
                piece = self.__board[row][col]
                if piece:
                    self.canvas.create_image(
                        col * size + offset,
                        row * size + offset,
                        image=piece.get_icon(),
                    )
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def init_ui(self):
        self.master.title("Шахматы")
        self.pack(fill=tk.BOTH, expand=1)
        self.draw()

    def __valid_bounds(self, pos: Position):
        return 0 <= pos.row <= self.cell_count and 0 <= pos.col <= self.cell_count

    def __valid_step_bounds(self, before: Position, after: Position):
        return self.__valid_bounds(before) and self.__valid_bounds(after)

    def get_current_color(self):
        if self.__stroke_number % 2 == 0:
            return PlayerColor.WHITE
        else:
            return PlayerColor.BLACK

    def __valid_step_and_color(self, pos: Position):
        piece = self.__board[pos.row][pos.col]
        return piece and self.get_current_color() == piece.get_color()

    def __is_figure(self, before: Position):
        return self.__board[before.row][before.col] is not None

    def __is_same_color(self, before: Position, after: Position):
        piece = self.__board[before.row][before.col]
        return piece and piece.is_same_color(self.__board[after.row][after.col])

    def __can_move(self, before: Position, after: Position):
        if self.__is_figure(after):
            return False

        return self.__board[before.row][before.col].can_move(before, after)

    def __can_kill(self, before: Position, after: Position):
        if (
            not self.__is_figure(after)
            or self.__is_same_color(before, after)
            or before.is_same(after)
        ):
            return False

        return self.__board[before.row][before.col].can_kill(before, after)

    def can_move(self, before: Position, after: Position):
        return (
            self.__valid_step_bounds(before, after)
            and self.__valid_step_and_color(before)
            and self.__is_figure(before)
            and (self.__can_move(before, after) or self.__can_kill(before, after))
        )

    def move(self, before: Position, after: Position):
        if not self.can_move(before, after):
            return

        self.__board[after.row][after.col] = self.__board[before.row][before.col]
        self.__board[before.row][before.col] = None
        self.__stroke_number += 1

        for row in self.__board:
            row.reverse()
        self.__board.reverse()
