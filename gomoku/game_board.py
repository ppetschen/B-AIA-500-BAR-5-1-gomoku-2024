from typing import List
from gomoku.config import PRINT_TABLE

class GameBoard:
    EMPTY = "."
    PLAYER = "1"
    AI = "2"

    def __init__(self, size: int = 20):
        self.size: int = size
        self.board: List[List[str]] = [
            [self.EMPTY for _ in range(self.size)] for _ in range(self.size)
        ]

    def initialize(self, size: int = 20) -> None:
        self.size = size
        self.board = [[self.EMPTY for _ in range(size)] for _ in range(size)]

    def opponent_move(self, x: int, y: int) -> None:
        if self.is_valid_move(x, y):
            self.set_position(x, y, self.PLAYER)

    def set_position(self, x: int, y: int, value: str) -> None:
        if self.is_valid_move(x, y):
            self.board[y][x] = value
        else:
            print(f"ERROR invalid move: {x}, {y}")

    def visualize(self) -> None:
        if (PRINT_TABLE == False):
            return
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

    def is_valid_move(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.size and 0 <= y < self.size and self.board[y][x] == self.EMPTY
        )

    def is_inside_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def validate_board(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] not in (self.EMPTY, self.PLAYER, self.AI):
                    return False
        return True
