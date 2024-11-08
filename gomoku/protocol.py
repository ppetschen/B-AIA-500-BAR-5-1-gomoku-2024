import sys
from typing import List, Optional, Tuple
from gomoku.game_board import GameBoard
from gomoku.ai import AI
import threading
import time
from gomoku.config import AI_THREAD_TIMEOUT


class CommandHandler:
    def __init__(self):
        self.board: Optional[GameBoard] = None
        self.game_board: GameBoard = GameBoard()
        self.ai: AI = AI(self.game_board)

    def listen_for_commands(self) -> None:
        for line in sys.stdin:
            command: List[str] = line.strip().split()
            if command:
                self.handle_command(command)

    def handle_command(self, command: List[str]) -> None:
        cmd_type: str = command[0]

        if cmd_type == "START":
            self.handle_start(command)
        elif cmd_type == "TURN":
            self.handle_turn(command)
        elif cmd_type == "BEGIN":
            self.handle_begin()
        elif cmd_type == "BOARD":
            self.handle_board()
        elif cmd_type == "END":
            self.handle_end()
        elif cmd_type == "ABOUT":
            self.handle_about()
        else:
            self.send_unknown()

    def handle_start(self, command: List[str]) -> None:
        try:
            size: int = int(command[1])
            if size == 20:
                self.game_board.initialize(size)
                print("OK")
                self.game_board.visualize()
            else:
                print("ERROR unsupported size")
        except ValueError:
            print("ERROR invalid size")
        sys.stdout.flush()

    def handle_turn(self, command: List[str]) -> None:
        try:
            x, y = map(int, command[1].split(","))
            if not self.game_board.is_valid_move(x, y):
                print(f"ERROR invalid move: {x}, {y}")
                return
            self.game_board.opponent_move(x, y)
            if not self.game_board.validate_board():
                raise ValueError("Board validation failed after opponent move")
            
            best_move = self.calculate_best_move()
            if best_move:
                print(f"{best_move[0]},{best_move[1]}")
                self.game_board.visualize()
                if not self.game_board.validate_board():
                    raise ValueError("Board validation failed after AI move")
            else:
                print("ERROR no valid move")
        except ValueError as e:
            print(f"ERROR {e}")
        sys.stdout.flush()

    def handle_begin(self) -> None:
        best_move = self.calculate_best_move()
        if best_move:
            print(f"{best_move[0]},{best_move[1]}")
            self.game_board.visualize()
            if not self.game_board.validate_board():
                print("ERROR board validation failed after AI move")
        else:
            print("ERROR no valid move")
        sys.stdout.flush()

    def handle_board(self) -> None:
        while True:
            line: str = sys.stdin.readline().strip()
            if line == "DONE":
                break
            x, y, field = map(int, line.split(","))
            try:
                self.game_board.set_position(x, y, str(field))
                if not self.game_board.validate_board():
                    raise ValueError("Board validation failed after setting position")
            except ValueError as e:
                print(f"ERROR {e}")

        move: Optional[Tuple[int, int]] = self.game_board.calculate_move()
        if move:
            print(f"{move[0]},{move[1]}")
            self.game_board.visualize()
            if not self.game_board.validate_board():
                print("ERROR board validation failed after AI move")
        else:
            print("ERROR no valid move")
        sys.stdout.flush()

    def handle_end(self) -> None:
        print("Shutting down.")
        sys.stdout.flush()
        sys.exit(0)

    def handle_about(self) -> None:
        print(
            'name="Gomoku", version="1.0", author="Joel Revuelta, Patricia Petschen, Lucia Jimenez", country="Spain"'
        )
        sys.stdout.flush()

    def send_unknown(self) -> None:
        print("UNKNOWN")
        sys.stdout.flush()

    def calculate_best_move(self) -> Optional[Tuple[int, int]]:
        best_move = [None]
        def run_ai():
            best_move[0] = self.ai.calculate_move()
        
        ai_thread = threading.Thread(target=run_ai)
        ai_thread.start()
        ai_thread.join(timeout=AI_THREAD_TIMEOUT)
        return best_move[0]
