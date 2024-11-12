from typing import Tuple, List
import sys

class InfoHandler:
    def __init__(self):
        self.timeout_turn: int = 0
        self.timeout_match: int = 0
        self.max_memory: int = 0
        self.time_left: int = 2147483647
        self.game_type: int = 0
        self.rule: int = 0
        self.evaluate: Tuple[int, int] = (0, 0)
        self.folder: str = ""
        self.unachievable_info: List[str] = []

    def handle_info(self, command: List[str]) -> None:
        if size := len(command) != 3:
            print("ERROR invalid number of arguments")
            sys.stdout.flush()
            return
        key, value = command[1], command[2]
        try:
            if key == "timeout_turn":
                self.timeout_turn = int(value)
            elif key == "timeout_match":
                self.timeout_match = int(value)
            elif key == "max_memory":
                self.max_memory = int(value)
            elif key == "time_left":
                self.time_left = int(value)
            elif key == "game_type":
                self.game_type = int(value)
            elif key == "rule":
                self.rule = int(value)
            elif key == "evaluate":
                self.evaluate = tuple(map(int, value.split(',')))
            elif key == "folder":
                self.folder = value
            else:
                print("ERROR unknown key")
                sys.stdout.flush()
                return
        except ValueError:
            print("ERROR invalid value")
            sys.stdout.flush()
            return