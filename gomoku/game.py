from gomoku.board import initialize_board

def start_game():
    board = initialize_board()
    print("Starting Gomoku game with an empty board:")
    for row in board:
        print(' '.join(row))

if __name__ == '__main__':
    start_game()
