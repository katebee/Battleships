
class Game(object):
    def __init__(self, ocean_size, fleet_size, max_turns):
        self.ocean_size = ocean_size
        self.fleet_size = fleet_size
        self.max_turns = max_turns

    def declare_ocean_size(self):
            print "The ocean is a {0} by {0} grid".format(self.ocean_size)


def declare_active_ships(player, fleet_size):
        if player.active_ships > 1:
            print "%d enemy ships detected! \n" % fleet_size
        else:
            print "%d enemy ship detected! \n" % fleet_size


class Board(object):
    def __init__(self, board_name):
        self.board_name = board_name

    @staticmethod
    def generate_empty_board(ocean_size):
        # this could use linked lists instead?
        board = [[" "]]
        for col in range(1, ocean_size + 1):
            board[0].append(str(col))           # Adds col numbers, also solves downstream user input vs. zero-base
        for row in range(1, ocean_size + 1):
            board.append(["O"] * ocean_size)
            board[row].insert(0, str(row))      # Adds row numbers, also solves downstream user input vs. zero-base
        return board

    @staticmethod
    def print_board(board):
        print
        for row in board:
            print " ".join(row)
        print


def print_board(board):
    print
    for row in board:
        print " ".join(row)
    print


def game_in_play(player_1, player_2, max_turns):
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


def run_game(player_1, player_2, max_turns):
    while not check_game_over((player_1, player_2)):
        for turn in range(1, max_turns + 1):
            print "TURN", turn
            current_turn(player=player_1, opponent=player_2)
            current_turn(player=player_2, opponent=player_1)
        break


def check_repeat_target(player, row, col):  # row and col will be passed as a tuple and will be in range
    return player.visible_board[row][col]


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