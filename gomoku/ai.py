from concurrent.futures import ThreadPoolExecutor
from typing import Tuple
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
            0: 0.1,
            1: 5,
            2: 50,
            3: 300,
            4: 15000
        }
        self.opponent_scores = {
            0: 0.1,
            1: 5,
            2: 50,
            3: 250,
            4: 2500
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
        evaluated_moves = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.evaluate_position, j, i)
                for i in range(self.game_board.size)
                for j in range(self.game_board.size)
                if self.game_board.board[i][j] == self.game_board.EMPTY
            ]
            for future in futures:
                j, i, score = future.result()
                evaluated_moves.append((j, i, score))
                if score > self.best_move.score:
                    self.best_move.x = j
                    self.best_move.y = i
                    self.best_move.score = score
                    if score >= 15000:
                        return
        evaluated_moves.sort(key=lambda move: move[2], reverse=True)
        top_moves = evaluated_moves[:5] + evaluated_moves[-5:]
        self.game_board.set_top_moves(top_moves)

    def evaluate_position(self, x: int, y: int) -> Tuple[int, int, int]:
        score = 0
        isBlocked = True
        for direction in (
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
        ):
            directionScore, directionBlocked = self.evaluate_direction(x, y, direction)
            score += directionScore
            if not directionBlocked:
                isBlocked = False
        if isBlocked:
            score = score * 0.01
        return x, y, score

    def evaluate_direction(self, x: int, y: int, direction: Tuple[int, int]) -> int:
        count_self, selfHasSpace, selfIsBlocked, selfPreBlocked = self.count_player_in_direction(x, y, direction, self.current_player)
        count_opponent, opponentHasSpace, opponentIsBlocked, opponentPreBlocked = self.count_player_in_direction(x, y, direction, self.opponent_player)

        selfScore = self.scores[count_self] * (0.8 if selfHasSpace else 1) * (0.5 if selfIsBlocked else 1) * (0.7 if selfPreBlocked else 1)
        opponentScore = self.opponent_scores[count_opponent] * (0.8 if opponentHasSpace else 1) * (0.5 if opponentIsBlocked else 1) * (0.7 if opponentPreBlocked else 1)

        return selfScore + opponentScore, selfIsBlocked and opponentIsBlocked

    def count_player_in_direction(
        self, x: int, y: int, direction: Tuple[int, int], player: str
    ) -> Tuple[int, bool, bool]:
        max_count = 0
        hasSpace = False
        isBlocked = True
        groupBlocked = False
        preBlocked = False

        for start in range(-4, 1):
            count = 0
            spaceInMiddle = False
            if groupBlocked:
                preBlocked = True
            groupBlocked = False
            for i in range(5):
                new_x = x + (start + i) * direction[0]
                new_y = y + (start + i) * direction[1]
                if not self.game_board.is_inside_board(new_x, new_y):
                    groupBlocked = True
                    break
                if self.game_board.board[new_y][new_x] == player:
                    count += 1
                    if spaceInMiddle:
                        hasSpace = True
                elif self.game_board.board[new_y][new_x] != self.game_board.EMPTY:
                    groupBlocked = True
                    break
                else:
                    if count > 0:
                        spaceInMiddle = True
            if not groupBlocked:
                isBlocked = False
                max_count = max(max_count, count)

        return max_count, hasSpace, isBlocked, preBlocked
