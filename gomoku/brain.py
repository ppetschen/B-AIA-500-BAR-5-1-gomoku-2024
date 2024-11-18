import sys
import threading
# from gomoku.protocol import CommandHandler
from gomoku.protocol_bonus import CommandHandlerBonus

def main():
    handler = CommandHandlerBonus()

    input_thread = threading.Thread(target=handler.listen_for_commands, daemon=True)
    input_thread.start()

    input_thread.join()

if __name__ == "__main__":
    main()
