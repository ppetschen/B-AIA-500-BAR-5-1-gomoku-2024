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
        if size := len(command) != 1:
            print("ERROR invalid number of arguments")
            sys.stdout.flush()
            return
        if not self.game_started:
            print("ERROR RESTART received before START")
            sys.stdout.flush()
            return

        #? if not self.game_ended:
        #?     if self.game_started:
        #?         print("ERROR you must finish the ongoing game first")

        try:
            self.game_board.initialize()
            self.board_locked = False
            self.begin_locked = False
            print("OK")
            self.game_board.visualize()
        except ValueError:
            print("ERROR invalid size")
