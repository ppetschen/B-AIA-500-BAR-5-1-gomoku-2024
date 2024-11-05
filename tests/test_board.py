# tests/test_board.py

import unittest
from gomoku.board import initialize_board

class TestBoard(unittest.TestCase):
    def test_initialize_board(self):
        board = initialize_board()
        self.assertEqual(len(board), 20)
        self.assertEqual(len(board[0]), 20)
        self.assertTrue(all(cell == '.' for row in board for cell in row))

if __name__ == '__main__':
    unittest.main()
