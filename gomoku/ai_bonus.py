from gomoku.ai import AI
from gomoku.game_board_bonus import GameBoardBonus

class AI_Bonus(AI):
    def __init__(self, game_board: GameBoardBonus):
        super().__init__(game_board)
        self.game_board: GameBoardBonus = game_board

    def simulate_move(self) -> None:
        evaluated_moves = []
        for i in range(self.game_board.size[1]):
            for j in range(self.game_board.size[0]):
                if self.game_board.board[i][j] == self.game_board.EMPTY:
                    score = self.evaluate_position(j, i)
                    evaluated_moves.append((j, i, score))
                    if score > self.best_move.score:
                        self.best_move.x = j
                        self.best_move.y = i
                        self.best_move.score = score
        evaluated_moves.sort(key=lambda move: move[2], reverse=True)
        top_moves = evaluated_moves[:5] + evaluated_moves[-5:]
        self.game_board.set_top_moves(top_moves)