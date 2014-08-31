from random import randint

board = []

for x in range(5):
    board.append(["O"] * 5)

def print_board(board):
    for row in board:
        print " ".join(row)

print "Let's play Battleship!"
print_board(board)
print

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)

for turn in range(4):
    print "Turn", turn + 1
    while True:
        try:
            guess_row = int(raw_input("Guess Row:")) - 1
            break
        except ValueError:
            print "That is not a valid coordinate!"
    while True:
        try:
            guess_col = int(raw_input("Guess Col:")) - 1
            break
        except ValueError:
            print "That is not a valid coordinate!"
    if guess_row == ship_row and guess_col == ship_col:
        board[ship_row][ship_col] = "X"
        print "Congratulations! You sunk my battleship!"
        print_board(board)
        break
    else:
        if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
            print "Oops, that's not even in the ocean."
        elif(board[guess_row][guess_col] == "-"):
            print "You guessed that one already."
            
        elif (guess_row == ship_row) and (guess_col == ship_col + 1 or guess_col == ship_col - 1):
            print "Phew, that was close... However, you missed my battleship!"
            board[guess_row][guess_col] = "-"
        elif (guess_col == ship_col) and (guess_row == ship_row + 1 or guess_row == ship_row - 1):
            print "Phew, that was close... However, you missed my battleship!"
            board[guess_row][guess_col] = "-"
        elif (guess_row == ship_row + 1 or guess_row == ship_row - 1) and (guess_col == ship_col + 1) or (guess_col == ship_col - 1):
            print "Phew, that was close... However, you missed my battleship!"
            board[guess_row][guess_col] = "-"
        else:
            print "You missed my battleship!"
            board[guess_row][guess_col] = "-"
    if turn == 3:
        print "GAME OVER - YOU LOSE"
        board[ship_row][ship_col] = "X"
        print "Here is where my battleship was hidden:"
        print_board(board)
    else:
        print_board(board)
        print