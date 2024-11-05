# tests/test_game.py

import unittest
from gomoku.game import start_game

class TestGame(unittest.TestCase):
    def test_start_game(self):
        self.assertIsNone(start_game())

if __name__ == '__main__':
    unittest.main()
