__author__ = 'Admin'

import config
import players


class Game(object):
    def __init__(self, ocean_size, fleet_size, max_turns):
        self.ocean_size = ocean_size
        self.fleet_size = fleet_size
        self.max_turns = max_turns

    def declare_ocean_size(self):
            print "The ocean is a {0} by {0} grid".format(self.ocean_size)

    @staticmethod
    def declare_active_ships(player):
            if player.active_ships > 1:
                print "%d enemy ships detected! \n" % player.active_ships
            else:
                print "%d enemy ship detected! \n" % player.active_ships


def run_game(player_1, player_2):
    while not check_game_over(player_1, player_2):
        for turn in range(1, config.max_turns + 1):
            print "TURN", turn
            current_turn(player=player_1, opponent=player_2)
            current_turn(player=player_2, opponent=player_1)
        break


def current_turn(player, opponent):
    opponent.visible_board.print_board()
    player.attack(opponent)
    if all_ships_destroyed(opponent):
        declare_winner(player)


def check_game_over(*players):
    for player in players:
        if all_ships_destroyed(player):
            return True
        return False


def all_ships_destroyed(player):
    if player.active_ships == 0:
        return True
    return False


def declare_winner(player):
    print "That was the last battleship..."
    print player.name.upper() + " WINS!"


# ############ GAME START #######################################

if __name__ == "__main__":
    # create a new game
    game = Game(ocean_size=config.ocean_size, fleet_size=config.fleet_size, max_turns=config.max_turns)

    # initialise players
    player_1 = players.HumanPlayer("HUMAN")
    player_2 = players.ComputerPlayer("COMPUTER")

    player_1.check_player_name()

    # start game - position ships and declare ocean and fleet size
    game.declare_ocean_size()

    player_1.private_board.print_board()

    player_1.position_fleet(config.fleet_size)
    player_2.position_fleet(config.fleet_size)

    game.declare_active_ships(player_2)

    run_game(player_1, player_2)