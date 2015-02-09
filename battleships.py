from random import randint

board = []
for x in range(5):
    board.append(["O"] * 5)

player = [] # Stores where the player is positioned and AI fire
for x in range(5):
    player.append(["O"] * 5)
    
def print_board(grid):
    for row in grid:
        print " ".join(row)

print "Let's play Battleship!"
print_board(board)
print # Formatting space for reading ease of player

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

# New function for hiding player ship
# Future versions to include cheat or god mode
print "Please decide the position of your battleship:"
while True:
    try:
        player_row = int(raw_input("Row:")) - 1
        if 0 <= player_row <= 5:
            break
        else:
            print "That's not even in the ocean..."
    except ValueError:
        print "That is not a valid coordinate!"

while True:
    try:
        player_col = int(raw_input("Col:")) - 1
        if 0 <= player_col <= 5:
            break
        else:
            print "That's not even in the ocean..."
    except ValueError:
        print "That is not a valid coordinate!"
    
player[player_row][player_col] = "X"
# print_board(player)

###########################################################

print "Positioning my battleship..."
ship_row = random_row(board)
ship_col = random_col(board)

# debugging mode!!! Edit this out before beta release!!
print ship_row + 1, ship_col + 1

for turn in range(1, 5):
    print "Turn", turn
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
            print "That was close... However, you missed my battleship!"
            board[guess_row][guess_col] = "-"
        elif (guess_col == ship_col) and (guess_row == ship_row + 1 or guess_row == ship_row - 1):
            print "That was close... However, you missed my battleship!"
            board[guess_row][guess_col] = "-"
        elif (guess_row == ship_row + 1 or guess_row == ship_row - 1) and (guess_col == ship_col + 1) or (guess_col == ship_col - 1):
            print "That was close... However, you missed my battleship!"
            board[guess_row][guess_col] = "-"
        else:
            print "You missed my battleship!"
            board[guess_row][guess_col] = "-"
            
    if turn % 3 == 0: # add fuction for return volley after x player turns
        print "Returning random fire!" 
        def hit_continue(Prompt="(Hit any key to continue)"):
            raw_input(Prompt)
        
        count = 0
        while count < 3:
            fire_row = randint(0, len(board[0]) - 1)
            fire_col = randint(0, len(board[0]) - 1)
            print "Firing at: %s, %s" % (fire_row, fire_col)

            if fire_row == player_row and fire_col == player_col:
                print "I hit your battleship! I win!"
                break
            else:
                print "It appears I missed..."
                player[fire_row][fire_col] = "-"
                count += 1
        print_board(player)
        print "Your turn!"
        
# Lose condition does not terminate game
    if turn == 7:
        print "GAME OVER - YOU LOSE"
        board[ship_row][ship_col] = "X"
        print "Here is where my battleship was hidden:"
        print_board(board)
        break
    else:
        print_board(board)
        print
