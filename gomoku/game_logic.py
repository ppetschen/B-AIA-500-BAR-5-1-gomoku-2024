import random

class GameBoard:
    EMPTY = '.'
    PLAYER = '1'
    AI = '2'

    def __init__(self, size=20):
        self.size = 20
        self.board = [(self.EMPTY for _ in range(self.size)) for _ in range(self.size)]

    def initialize(self, size=20):
        self.size = size
        self.board = [[self.EMPTY for _ in range(size)] for _ in range(size)]

    def opponent_move(self, x, y):
        if self.is_valid_move(x, y):
            self.set_position(x, y, self.PLAYER)


    def calculate_move(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.EMPTY:
                    self.set_position(i, j, self.AI)
                    return j, i

    def set_position(self, x, y, value):
        if self.is_valid_move(x, y):
            self.board[y][x] = value
        else:
            print(f"ERROR invalid move: {x}, {y}")

    def visualize(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[y][x] == self.EMPTY
    
    def validate_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] not in (self.EMPTY, self.PLAYER, self.AI):
                    return False
        return True
