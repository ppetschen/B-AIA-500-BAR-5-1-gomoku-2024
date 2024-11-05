import sys
import threading
from gomoku.protocol import CommandHandler

def main():
    handler = CommandHandler()

    input_thread = threading.Thread(target=handler.listen_for_commands, daemon=True)
    input_thread.start()

    input_thread.join()

if __name__ == "__main__":
    main()
