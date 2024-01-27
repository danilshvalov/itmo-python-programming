import tkinter as tk

from chesspy.board import Board


def main():
    root = tk.Tk()
    cell_count = 8
    cell_size = 100
    window_size = cell_count * cell_size

    board = Board(root, cell_count, cell_size)
    root.geometry(f"{window_size}x{window_size}+400+0")
    root.mainloop()


if __name__ == "__main__":
    main()
