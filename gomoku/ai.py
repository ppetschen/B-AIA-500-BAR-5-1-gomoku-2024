from typing import Optional, Tuple
from gomoku.game_board import GameBoard
import time
import threading
from gomoku.config import AI_THREAD_TIMEOUT


class BestMove:
    def __init__(self, x: int = 0, y: int = 0, score: int = 0):
        self.x = x
        self.y = y
        self.score = score

    def reset(self):
        self.x = 0
        self.y = 0
        self.score = 0


class AI:
    def __init__(self, game_board: GameBoard):
        self.game_board: GameBoard = game_board
        self.best_move: BestMove = BestMove()
        self.scores = {
            0: 0,
            1: 1,
            2: 10,
            3: 100,
            4: 10000,
            5: 100000,
        }
        self.enemy_scores = {
            0: 0,
            1: 1,
            2: 10,
            3: 100,
            4: 1000,
            5: 10000,
        }

    def calculate_move(self, player: str) -> Tuple[int, int]:
        self.best_move.reset()
        self.current_player = player
        self.opponent_player = self.game_board.PLAYER1 if player == self.game_board.PLAYER2 else self.game_board.PLAYER2
        simulation_thread = threading.Thread(target=self.run_simulations)
        simulation_thread.start()
        simulation_thread.join(timeout=AI_THREAD_TIMEOUT)
        self.game_board.set_position(
            self.best_move.x, self.best_move.y, player
        )
        return [self.best_move.x, self.best_move.y]

    def run_simulations(self):
        start_time = time.time()
        while time.time() - start_time < AI_THREAD_TIMEOUT:
            self.simulate_move()
            return

    def simulate_move(self) -> None:
        for i in range(self.game_board.size):
            for j in range(self.game_board.size):
                if self.game_board.board[i][j] == self.game_board.EMPTY:
                    score = self.evaluate_position(j, i)
                    if score > self.best_move.score:
                        self.best_move.x = j
                        self.best_move.y = i
                        self.best_move.score = score

    def evaluate_position(self, x: int, y: int) -> int:
        score = 0
        for direction in (
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
            (-1, 0),
            (0, -1),
            (-1, -1),
            (-1, 1),
        ):
            score += self.evaluate_direction(x, y, direction)
        return score

    def evaluate_direction(self, x: int, y: int, direction: Tuple[int, int]) -> int:
        count_self = self.count_player_in_direction(x, y, direction, self.current_player)
        count_enemy = self.count_player_in_direction(
            x, y, direction, self.opponent_player
        )
        return self.scores[count_self] + self.enemy_scores[count_enemy]

    def count_player_in_direction(
        self, x: int, y: int, direction: Tuple[int, int], player: str
    ):
        count = 0
        for i in range(1, 5):
            if not self.game_board.is_inside_board(
                x + i * direction[0], y + i * direction[1]
            ):
                break
            if (
                self.game_board.board[y + i * direction[1]][x + i * direction[0]]
                == player
            ):
                count += 1
            else:
                break
        return count
