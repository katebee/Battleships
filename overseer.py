

def new_game(size_ocean, size_fleet, turn_max):
    global ocean_size
    global fleet_size
    global max_turns
    ocean_size = size_ocean
    fleet_size = size_fleet
    max_turns = turn_max


def declare_ocean_size():
        print "The ocean is a {0} by {0} grid".format(ocean_size)


def declare_active_ships(player):
        if player.active_ships > 1:
            print "%d enemy ships detected! \n" % fleet_size
        else:
            print "%d enemy ship detected! \n" % fleet_size


def print_board(grid):
    print
    for row in grid:
        print " ".join(row)
    print


def game_in_play(player_1, player_2):
    for turn in range(1, max_turns + 1):
        print_board(player_2.visible_board)
        print "TURN", turn
        player_1.attack(opponent=player_2)
        if not player_2:
            break
        print_board(player_2.visible_board)
        player_2.attack(opponent=player_1)
        if not player_1:
            break


def start_game(player_1, player_2):
    declare_ocean_size()
    print_board(player_1.private_board)
    player_1.position_fleet(fleet_size)
    print_board(player_1.private_board)
    player_2.position_fleet(fleet_size)
    declare_active_ships(player_2)


def run_game(player_1, player_2):
    while not check_game_over((player_1, player_2)):
        for turn in range(1, max_turns + 1):
            print "TURN", turn
            current_turn(player=player_1, opponent=player_2)
            current_turn(player=player_2, opponent=player_1)
        break


def check_repeat_target(player, row, col):  # row and col will be passed as a tuple and will be in range
    return player.visible_board[row][col]


def check_target_location(player, row, col):
        if (row < 1 or row > ocean_size) or (col < 1 or col > ocean_size):
            # That's not even in the ocean...
            return False
        elif player.visible_board[row][col] == "-" or player.visible_board[row][col] == "X":
            # You guessed that one already
            return "REPEAT"
        elif player.private_board[row][col] == "X":
            # Hit!
            player.visible_board[row][col] = "X"
            player.active_ships -= 1
            return True
        else:
            # Missed
            player.visible_board[row][col] = "-"
            return False


def current_turn(player, opponent):
    print_board(opponent.visible_board)
    player.attack(opponent)


def check_game_over(players):
    for player in players:
        if all_ships_destroyed(player):
            return True
        return False


def end_game(player, opponent):
    if all_ships_destroyed(opponent):
        declare_winner(player)
        return True
    return False


def all_ships_destroyed(player):
    if player.active_ships == 0:
        return True
    return False


def declare_winner(player):
    print "That was the last battleship..."
    print player.name.upper() + " WINS!"