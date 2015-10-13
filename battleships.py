__author__ = 'Admin'
import re
from random import randint


class Game(object):
    pass

    @staticmethod
    def set_ocean_size(size):
        global ocean_size
        ocean_size = size

    @staticmethod
    def set_fleet_size(size):
        global fleet_size
        fleet_size = size

    @staticmethod
    def generate_empty_board():
        # linked lists
        board = [[" "]]
        for col in range(1, ocean_size + 1):
            board[0].append(str(col))           # Adds col numbers, also solves downstream user input vs. zero-base
        for row in range(1, ocean_size + 1):
            board.append(["O"] * ocean_size)
            board[row].insert(0, str(row))      # Adds row numbers, also solves downstream user input vs. zero-base
        return board

    @staticmethod
    def print_board(grid):
        print
        for row in grid:
            print " ".join(row)
        print


class Overseer(object):  # tracks whose turn it is and declares winner.

    def game_in_play(self):
        for turn in range(1, 5):
            print "TURN", turn
            Game.print_board(player_2.visible_board)
            player_1.attack(opponent=player_2)
            if not player_2:
                break
            Game.print_board(player_2.visible_board)
            player_2.attack(opponent=player_1)
            if not player_1:
                break

    def declare_winner(self, *players):
        pass


class Player(object):
    def __init__(self, player_name):
        self.name = player_name
        self.human = False
        self.private_board = Game.generate_empty_board()  # makes a [] Add an integer to g_e_b to specify size of board
        self.visible_board = Game.generate_empty_board()  # call this one to show other player
        self.active_ships = 0
        self.guessed_row = 0
        self.guessed_col = 0

    @staticmethod
    def random_location():
        return randint(1, ocean_size)

    def guess_coordinate(self, coordinate):
        if self.human:
            while True:
                try:
                    return int(raw_input("Guess %s: " % coordinate))
                except ValueError:
                    print "That is not a valid coordinate!"
        else:
            return randint(1, ocean_size)

    def guess_location(self):
        return (self.guess_coordinate("Row"), self.guess_coordinate("Col"))  # Returns a tuple to check

    def attack(self, opponent):
        coordinates = self.guess_location()
        opponent.check_target_location(*coordinates)

    def __nonzero__(self):
        return bool(self.active_ships)


class HumanPlayer(Player):
    def __init__(self, player_name):
        super(HumanPlayer, self).__init__(player_name)
        self.human = True

    def check_player_name(self):
        name_check = True
        while name_check:
            player_name = raw_input('What is your name? ')
            player_name = player_name.strip()
            if not re.match("^[A-Za-z]*$", player_name):
                print "Error! Only letters a-z allowed!"
            elif len(player_name) > 15:
                print "Error! Only 15 characters allowed!"
            elif player_name == "":
                self.name = "Anon"
                name_check = False
            else:
                self.name = player_name
                name_check = False
        print "Hi " + self.name + "! Let's play Battleship!"

    def position_ship(self):
        print "Please decide the position of your battleship"
        collision_check = True  # check that no ship is already there
        while collision_check:
            row_check = True
            col_check = True
            while row_check:
                try:
                    position_row = int(raw_input("Row: "))
                    if 1 <= position_row <= 5:
                        row_check = False
                    else:
                        print "That's not even in the ocean..."
                except ValueError:
                    print "That is not a valid coordinate!"
            while col_check:
                try:
                    position_col = int(raw_input("Col: "))
                    if 1 <= position_col <= 5:
                        col_check = False
                    else:
                        print "That's not even in the ocean..."
                except ValueError:
                    print "That is not a valid coordinate!"
            if self.private_board[position_row][position_col] == "X":
                print "there is already a ship at this location!"
            else:
                print "Ship positioned at %d:%d " % (position_row, position_col)
                self.private_board[position_row][position_col] = "X"
                self.active_ships += 1
                collision_check = False

    def position_fleet(self, fleet):
        print "The ocean is a {0} by {0} grid".format(ocean_size)
        if fleet > 1:
            print "you have %d ships" % fleet
        else:
            print "you have %d ship" % fleet
        for ship in range(fleet):
            self.position_ship()

    def check_target_location(self, row, col):  # row and col will be passed as a tuple
        if (row < 1 or row > 5) or (col < 1 or col > 5):
            print "Oops, that's not even in the ocean."
        elif self.visible_board[row][col] == "-":
                print "You guessed that one already."
        elif self.private_board[row][col] == "X":
            self.visible_board[row][col] = "X"
            print "A battleship was hit!"  # return hit?
            Game.print_board(self.visible_board)
            self.active_ships -= 1
        else:
            print "You missed my battleship!"
            self.visible_board[row][col] = "-"


class ComputerPlayer(Player):
    def __init__(self, player_name):
        super(ComputerPlayer, self).__init__(player_name)
        self.human = False

    def position_fleet(self, fleet):
        if fleet > 1:
            print "%d enemy ships detected!" % fleet
        else:
            print "%d enemy ship detected!" % fleet
        for ship in range(fleet):
            self.position_ship()

    def position_ship(self):
        position_row = self.random_location()
        position_col = self.random_location()
        if self.private_board[position_row][position_col] == "X":
            self.position_ship()
        else:
            self.private_board[position_row][position_col] = "X"
            self.active_ships += 1

    def check_target_location(self, row, col):  # row and col will be passed as a tuple
        if (row < 1 or row > 5) or (col < 1 or col > 5):
            print "COMPUTER: Oops, that's not even in the ocean."
        elif self.visible_board[row][col] == "-":
            print "COMPUTER: You guessed that one already."
        elif self.private_board[row][col] == "X":
            self.visible_board[row][col] = "X"
            print "COMPUTER: Congratulations! You sunk my battleship!"  # return hit?
            Game.print_board(self.visible_board)
            self.active_ships -= 1
        else:
            print "COMPUTER: You missed my battleship!"
            self.visible_board[row][col] = "-"


# ocean size should be able to be adjusted and have downstream effects.
# Need to check ocean size when placing ships, and when selecting attack site.
# add functions to determine size of the ocean and number of ships each player has?
# Expand game options to larger ocean and more ships in later iterations?





# ############ GAME START #######################################

if __name__ == "__main__":
    # take player name and generate player and AI
    Game.set_ocean_size(5)
    # game should initialise players
    player_1 = HumanPlayer('Player 1')
    player_2 = ComputerPlayer('Computer')
    # add something to indicate the size of the ocean / row col count
    # you have x ships and the ocean is y * z

    #  place ships
    player_1.check_player_name()
    player_1.position_fleet(fleet=2)
    Game.print_board(player_1.private_board)

    player_2.position_fleet(fleet=2)
    Game.print_board(player_2.visible_board)
    # show the player their board before commencing game

    # play game

    # AI positions battleship

    Game.print_board(player_2.private_board)

    Overseer.game_in_play()
