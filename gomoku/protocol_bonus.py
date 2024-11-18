import sys
from typing import List
from gomoku.game_board import GameBoard
from gomoku.ai import AI
import threading
import time
from gomoku.config import AI_THREAD_TIMEOUT
from gomoku.protocol import CommandHandler

class CommandHandlerBonus(CommandHandler):
    def __init__(self):
        super().__init__()

    def handle_command(self, command: List[str]) -> None:
        cmd_type: str = command[0]
        if cmd_type == "RESTART":
            self.handle_restart(command)
        else:
            return super().handle_command(command)

    def handle_restart(self, command: List[str]) -> None:
        #^ TEMP Copy of the handle_start method from protocol.py file
        if size := len(command) != 2:
            print("ERROR invalid number of arguments")
            sys.stdout.flush()
            return
        try:
            size: int = int(command[1])
            if size == 20:
                self.game_board.initialize(size)
                self.game_started = True
                self.board_locked = False
                self.begin_locked = False
                print("OK [RESTART]")
                self.game_board.visualize()
            else:
                print("ERROR unsupported size [RESTART]")
        except ValueError:
            print("ERROR invalid size")
