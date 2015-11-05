
import re  # used in check_player_name to check for allowed characters

from random import randint

import config
import board


class Player(object):
    def __init__(self, player_name):
        self.name = player_name
        self.private_board = board.Board(config.ocean_size)
        self.visible_board = board.Board(config.ocean_size)  # call this one to show other player
        self.active_ships = 0
        self.guessed_row = 0
        self.guessed_col = 0

    @staticmethod
    def random_location():
        return randint(1, config.ocean_size)

    def get_coordinate(self, prompt):
        return self.random_location()

    def guess_location(self):
        return (self.get_coordinate("Guess Row: "), self.get_coordinate("Guess Col: "))  # Returns a tuple to check

    def repeat_location_check(self, row, col):  # row and col will be passed as a tuple and will be in range
        return self.visible_board.board[row][col]

    def attack(self, opponent):
        coordinates = self.guess_location()
        target = opponent.repeat_location_check(*coordinates)
        if target == "-" or target == "X":
            self.attack(opponent)
        else:
            print "Missile fired at %d:%d!" % coordinates
            opponent.check_target_location(*coordinates)


class HumanPlayer(Player):
    def __init__(self, player_name):
        super(HumanPlayer, self).__init__(player_name)

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

    def collision_check(self, row, col):
        if self.private_board.board[row][col] == "X":
            print "There is already a ship at this location!"
            return True
        return False

    def position_ship(self):
        print "Please decide the position of your battleship"
        row = self.get_coordinate("Row: ")  # check int and that it is in range (1 to ocean_size)
        col = self.get_coordinate("Col: ")
        if self.collision_check(row, col):
            print "there is already a ship at this location!"
            self.position_ship()
        else:
            print "Ship positioned at %d:%d " % (row, col)
            self.private_board.board[row][col] = "X"
            self.active_ships += 1

    def get_coordinate(self, prompt):  # overrides the random number generator from the player class
        while True:
            try:
                user_input = int(raw_input(prompt))
                if 1 <= user_input <= config.ocean_size:
                    return user_input
                else:
                    print "That's not even in the ocean... Please enter a number from 1 to %s!" % config.ocean_size
            except ValueError:
                print "That is not a number!"

    def position_fleet(self, fleet_size):
        if fleet_size > 1:
            print "you have %d ships" % fleet_size
        else:
            print "you have %d ship" % fleet_size
        for ship in range(fleet_size):
            self.position_ship()

    def check_target_location(self, row, col):  # row and col will be passed as a tuple
        if (1 > row > config.ocean_size) or (1 > col > config.ocean_size):
            print "...Oops, that's not even in the ocean."
        elif self.visible_board.board[row][col] == "-" or self.visible_board.board[row][col] == "X":
                print "...You guessed that one already."
        elif self.private_board.board[row][col] == "X":
            self.visible_board.board[row][col] = "X"
            print "...A battleship was hit!"  # return hit?
            self.visible_board.print_board()
            self.active_ships -= 1
        else:
            print "...It missed!"
            self.visible_board.board[row][col] = "-"


class ComputerPlayer(Player):
    def __init__(self, player_name):
        super(ComputerPlayer, self).__init__(player_name)

    def position_fleet(self, fleet_size):
        for ship in range(fleet_size):
            self.position_ship()

    def position_ship(self):
        row = self.random_location()
        col = self.random_location()
        if self.private_board.board[row][col] == "X":
            self.position_ship()
        else:
            self.private_board.board[row][col] = "X"
            self.active_ships += 1

    def check_target_location(self, row, col):  # row and col will be passed as a tuple
        if (1 > row > config.ocean_size) or (1 > col > config.ocean_size):
            print "COMPUTER: Oops, that's not even in the ocean."
        elif self.visible_board.board[row][col] == "-" or self.visible_board.board[row][col] == "X":
            print "COMPUTER: You guessed that one already."
        elif self.private_board.board[row][col] == "X":
            self.visible_board.board[row][col] = "X"
            print "COMPUTER: Congratulations! You sunk my battleship!"  # return hit?
            self.visible_board.print_board()
            self.active_ships -= 1
        else:
            print "COMPUTER: You missed my battleship!"
            self.visible_board.board[row][col] = "-"
