from typing import List, Tuple
from gomoku.game_board import GameBoard
from gomoku.config import PRINT_TABLE
from gomoku.config import TOP_MOVES

class GameBoardBonus(GameBoard):

    def __init__(self, size: Tuple[int, int] = (20, 20)):
        self.size: Tuple[int, int] = size
        self.board: List[List[str]] = [
            [self.EMPTY for _ in range(self.size[0])] for _ in range(self.size[1])
        ]
        self.top_moves: List[Tuple[int, int, int]] = []  # Top moves (x, y, score)

    def initialize(self, size: Tuple[int, int] = (20, 20)) -> None:
        self.size = size
        self.board = [[self.EMPTY for _ in range(size[0])] for _ in range(size[1])]
        self.top_moves = []

    def set_top_moves(self, top_moves: List[Tuple[int, int, int]]) -> None:
        self.top_moves = top_moves
    
    def visualize(self) -> None:
        if not PRINT_TABLE:
            return

        board_rows = [" ".join(str(cell) for cell in row) for row in self.board]

        best_moves_table = []
        worst_moves_table = []

        if TOP_MOVES and self.top_moves:
            best_moves_table.append("Top 5 BEST Moves:")
            best_moves_table.append(f"{'Rank':<5} {'X':<5} {'Y':<5} {'Score':<10}")
            best_moves_table.append("-" * 30)
            best_moves_table += [
                f"{rank:<5} {x:<5} {y:<5} {score:<10.2f}"
                for rank, (x, y, score) in enumerate(self.top_moves[:5], start=1)
            ]

            worst_moves_table.append("Top 5 WORST Moves:")
            worst_moves_table.append(f"{'Rank':<5} {'X':<5} {'Y':<5} {'Score':<10}")
            worst_moves_table.append("-" * 30)
            worst_moves_table += [
                f"{rank:<5} {x:<5} {y:<5} {score:<10.2f}"
                for rank, (x, y, score) in enumerate(self.top_moves[-5:], start=1)
            ]

        combined_table = best_moves_table + [""] + worst_moves_table if TOP_MOVES and self.top_moves else []

        while len(combined_table) < len(board_rows):
            combined_table.append("")

        visualization = "\n".join(
            f"{board_row:<40} {table_row}"
            for board_row, table_row in zip(board_rows, combined_table)
        )
    
        visualization += "\n" + "\n".join(combined_table[len(board_rows):])
    
        print(visualization)


    def is_valid_move(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.size[0] and 0 <= y < self.size[1] and self.board[y][x] == self.EMPTY
        )

    def is_inside_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def validate_board(self) -> bool:
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.board[i][j] not in (self.EMPTY, self.PLAYER1, self.PLAYER2):
                    return False
        return True
