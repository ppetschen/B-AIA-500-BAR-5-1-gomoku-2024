import random

class GameBoard:
    def __init__(self):
        self.size = 20
        self.board = []

    def initialize(self, size=20):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def opponent_move(self, x, y):
        self.board[y][x] = 2

    def calculate_move(self):
        empty_positions = [(x, y) for y in range(self.size) for x in range(self.size) if self.board[y][x] == 0]
        return random.choice(empty_positions) if empty_positions else (0, 0)

    def set_position(self, x, y, value):
        self.board[y][x] = value
