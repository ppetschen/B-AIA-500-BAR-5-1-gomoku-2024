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
            0: 1,
            1: 5,
            2: 20,
            3: 150,
            4: 15000
        }
        self.opponent_scores = {
            0: 1,
            1: 5,
            2: 20,
            3: 150,
            4: 1500
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
        evaluated_moves.sort(key=lambda move: move[2], reverse=True)
        top_moves = evaluated_moves[:5] + evaluated_moves[-5:]
        self.game_board.set_top_moves(top_moves)

    def evaluate_position(self, x: int, y: int) -> Tuple[int, int, int]:
        score = 0
        for direction in (
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
        ):
            score += self.evaluate_direction(x, y, direction)
        return x, y, score

    def evaluate_direction(self, x: int, y: int, direction: Tuple[int, int]) -> int:
        count_self_1, selfHasSpace_1, selfIsBlocked_1 = self.count_player_in_direction(x, y, direction, self.current_player)
        count_self_2, selfHasSpace_2, selfIsBlocked_2 = self.count_player_in_direction(x, y, (-direction[0], -direction[1]), self.current_player)
        count_self = count_self_1 + count_self_2
        selfIsBlocked = selfIsBlocked_1 and selfIsBlocked_2
        selfIsHalfBlocked = selfIsBlocked_1 or selfIsBlocked_2
        selfHasSpace = selfHasSpace_1 or selfHasSpace_2
        selfHalfSpace = selfHasSpace_1 and selfHasSpace_2

        count_opponent_1, opponentHasSpace_1, opponentIsBlocked_1 = self.count_player_in_direction(x, y, direction, self.opponent_player)
        count_opponent_2, opponentHasSpace_2, opponentIsBlocked_2 = self.count_player_in_direction(x, y, (-direction[0], -direction[1]), self.opponent_player)
        count_opponent = count_opponent_1 + count_opponent_2
        opponentIsBlocked = opponentIsBlocked_1 and opponentIsBlocked_2
        opponentIsHalfBlocked = opponentIsBlocked_1 or opponentIsBlocked_2
        opponentHasSpace = opponentHasSpace_1 or opponentHasSpace_2
        opponentHalfSpace = opponentHasSpace_1 and opponentHasSpace_2

        selfScore = self.scores[count_self] * (0.8 if selfHasSpace else 1) * (0.9 if selfHalfSpace else 1) * (0.5 if selfIsBlocked else 1) * (0.9 if selfIsHalfBlocked else 1)
        opponentScore = self.opponent_scores[count_opponent] * (0.8 if opponentHasSpace else 1) * (0.9 if opponentHalfSpace else 1) * (0.5 if opponentIsBlocked else 1) * (0.9 if opponentIsHalfBlocked else 1)

        return selfScore + opponentScore

    def count_player_in_direction(
        self, x: int, y: int, direction: Tuple[int, int], player: str
    ) -> Tuple[int, bool, bool]:
        count = 0
        hasSpace = False
        spaceInMiddle = False
        isBlocked = False
        for i in range(1, 5):
            new_x = x + i * direction[0]
            new_y = y + i * direction[1]
            if not self.game_board.is_inside_board(new_x, new_y):
                isBlocked = True
                break
            if self.game_board.board[new_y][new_x] == player:
                count += 1
                if spaceInMiddle:
                    hasSpace = True
            elif self.game_board.board[new_y][new_x] != self.game_board.EMPTY:
                isBlocked = True
                if spaceInMiddle:
                    hasSpace = True
                break
            else:
                spaceInMiddle = True
        return count, hasSpace, isBlocked
