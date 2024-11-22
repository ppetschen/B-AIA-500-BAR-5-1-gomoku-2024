from typing import List, Tuple
from gomoku.config import PRINT_TABLE
from gomoku.config import TOP_MOVES

class GameBoard:
    EMPTY = "."
    PLAYER1 = "1"
    PLAYER2 = "2"

    def __init__(self, size: int = 20):
        self.size: int = size
        self.board: List[List[str]] = [
            [self.EMPTY for _ in range(self.size)] for _ in range(self.size)
        ]
        self.top_moves: List[Tuple[int, int, int]] = []

    def initialize(self, size: int = 20) -> None:
        self.size = size
        self.board = [[self.EMPTY for _ in range(size)] for _ in range(size)]

    def opponent_move(self, x: int, y: int) -> None:
        if self.is_valid_move(x, y):
            self.set_position(x, y, self.PLAYER1)

    def set_position(self, x: int, y: int, value: str) -> None:
        if self.is_valid_move(x, y):
            self.board[y][x] = value
        else:
            print(f"ERROR invalid move: {x}, {y}")

    def set_top_moves(self, top_moves: List[Tuple[int, int, int]]) -> None:
        self.top_moves = top_moves

    def visualize(self) -> None:
        if (PRINT_TABLE == False):
            return
        board_rows = [" ".join(str(cell) for cell in row) for row in self.board]
        best_moves_table = []
        worst_moves_table = []
        if TOP_MOVES and self.top_moves:
            best_moves_table.append("Top 5 BEST Moves:")
            best_moves_table.append(f"{'Rank':<5} {'X':<5} {'Y':<5} {'Score':<10}")
            best_moves_table.append("-" * 30)
            best_moves_table += [
                f"{rank:<5} {x:<5} {y:<5} {score:<10}"
                for rank, (x, y, score) in enumerate(self.top_moves[:5], start=1)
            ]
            worst_moves_table.append("Top 5 WORST Moves:")
            worst_moves_table.append(f"{'Rank':<5} {'X':<5} {'Y':<5} {'Score':<10}")
            worst_moves_table.append("-" * 30)
            worst_moves_table += [
                f"{rank:<5} {x:<5} {y:<5} {score:<10}"
                for rank, (x, y, score) in enumerate(self.top_moves[-5:], start=1)
            ]

        combined_table = best_moves_table + [""] + worst_moves_table if TOP_MOVES and self.top_moves else []

        while len(combined_table) < 20:
            combined_table.append("")

        print("\n".join(
            f"{board_row:<40} {table_row}"
            for board_row, table_row in zip(board_rows, combined_table)
        ))

    def is_valid_move(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.size and 0 <= y < self.size and self.board[y][x] == self.EMPTY
        )

    def is_inside_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def validate_board(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] not in (self.EMPTY, self.PLAYER1, self.PLAYER2):
                    return False
        return True
