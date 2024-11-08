# tests/test_board.py

import unittest
from gomoku.game_board import GameBoard

class TestBoard(unittest.TestCase):
    def test_initialize_board(self):
        board = GameBoard()
        self.assertEqual(len(board.board), 20)
        self.assertEqual(len(board.board), 20)
        self.assertTrue(all(cell == '.' for row in board.board for cell in row))

if __name__ == '__main__':
    unittest.main()
