import sys
from typing import List, Tuple
# from gomoku.ai import AI
import threading
import time
from gomoku.ai_bonus import AI_Bonus
from gomoku.config import AI_THREAD_TIMEOUT
from gomoku.game_board_bonus import GameBoardBonus
from gomoku.protocol import CommandHandler

class CommandHandlerBonus(CommandHandler):
    def __init__(self):
        super().__init__()
        self.game_board: GameBoardBonus = GameBoardBonus()
        self.ai: AI_Bonus = AI_Bonus(self.game_board)

    def handle_command(self, command: List[str]) -> None:
        cmd_type: str = command[0]
        if cmd_type == "RECSTART":
            self.handle_recstart(command)
        elif cmd_type == "RESTART":
            self.handle_restart(command)
        else:
            super().handle_command(command)
    
    # handle different sizes
    def handle_start(self, command: List[str]) -> None:
        if size := len(command) != 2:
            print("ERROR invalid number of arguments")
            sys.stdout.flush()
            return
        try:
            size: int = int(command[1])
            if size > 4:
                self.game_board.initialize((size, size))
                self.game_started = True
                self.board_locked = False
                self.begin_locked = False
                print("OK")
                self.game_board.visualize()
            else:
                print("ERROR unsupported size")
        except ValueError:
            print("ERROR invalid size")
        sys.stdout.flush()

    def handle_recstart(self, command: List[str]) -> None:
        # def handle_start(self, command: List[str]) -> None:
        if size := len(command) != 2:
            print("ERROR invalid number of arguments")
            sys.stdout.flush()
            return
        try:
            x, y = map(int, command[1].split(","))
            size: Tuple[int, int] = (int(x), int(y))
            #? self.game_board.size = 0
            if size[0] != size[1] and size[0] > 4 and size[1] > 4:
                self.game_board.initialize((x, y))
                self.game_started = True
                self.board_locked = False
                self.begin_locked = False
                print("OK")
                self.game_board.visualize()
            else:
                print("ERROR unsupported size RECSTART")
                print("size: ", size)
        except ValueError:
            print("ERROR invalid size")
        sys.stdout.flush()


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
            self.game_board.initialize(self.game_board.size)
            self.board_locked = False
            self.begin_locked = False
            print("OK")
            self.game_board.visualize()
        except ValueError:
            print("ERROR invalid size")
    
