
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


def game_in_play(player_1, player_2, max_turns):
    for turn in range(1, max_turns + 1):
        player_2.visible_board.print_board()
        print "TURN", turn
        player_1.attack(opponent=player_2)
        if not player_2:
            break
        player_2.visible_board.print_board()
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


def current_turn(player, opponent):
    opponent.visible_board.print_board()
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