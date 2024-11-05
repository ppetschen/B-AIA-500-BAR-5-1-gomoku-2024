import sys
from gomoku.game_logic import GameBoard

class CommandHandler:
    def __init__(self):
        self.board = None
        self.game_board = GameBoard()

    def listen_for_commands(self):
        for line in sys.stdin:
            command = line.strip().split()
            if command:
                self.handle_command(command)

    def handle_command(self, command):
        cmd_type = command[0]
        
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

    def handle_start(self, command):
        try:
            size = int(command[1])
            if size == 20:
                self.game_board.initialize(size)
                print("OK")
            else:
                print("ERROR unsupported size")
        except ValueError:
            print("ERROR invalid size")
        sys.stdout.flush()

    def handle_turn(self, command):
        x, y = map(int, command[1].split(","))
        self.game_board.opponent_move(x, y)
        next_move = self.game_board.calculate_move()
        print(f"{next_move[0]},{next_move[1]}")
        sys.stdout.flush()

    def handle_begin(self):
        move = self.game_board.calculate_move()
        print(f"{move[0]},{move[1]}")
        sys.stdout.flush()

    def handle_board(self):
        while True:
            line = sys.stdin.readline().strip()
            if line == "DONE":
                break
            x, y, field = map(int, line.split(","))
            self.game_board.set_position(x, y, field)

        move = self.game_board.calculate_move()
        print(f"{move[0]},{move[1]}")
        sys.stdout.flush()

    def handle_end(self):
        print("Shutting down.")
        sys.stdout.flush()
        sys.exit(0)

    def handle_about(self):
        print('name="Gomoku", version="1.0", author="Joel Revuelta, Patricia Petschen, Lucia Jimenez", country="Spain"')
        sys.stdout.flush()

    def send_unknown(self):
        print("UNKNOWN")
        sys.stdout.flush()
