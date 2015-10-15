__author__ = 'Admin'
import re  # used in check_player_name to check for allowed characters
import overseer
from random import randint


class Player(object):
    def __init__(self, player_name):
        self.name = player_name
        self.private_board = self.generate_empty_board(overseer.ocean_size)
        self.visible_board = self.generate_empty_board(overseer.ocean_size)  # call this one to show other player
        self.active_ships = 0
        self.guessed_row = 0
        self.guessed_col = 0

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
    def random_location():
        return randint(1, overseer.ocean_size)

    def guess_coordinate(self, coordinate):
        return self.random_location()

    def guess_location(self):
        return (self.guess_coordinate("Row"), self.guess_coordinate("Col"))  # Returns a tuple to check

    def attack(self, opponent):
        coordinates = self.guess_location()
        target = overseer.check_repeat_target(opponent, *coordinates)
        if target == "-" or target == "X":
            self.attack(opponent)

        overseer.check_target_location(opponent, *coordinates)

        print "Missile fired at %d:%d!" % coordinates


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

    def collision_check(self, row, col):
        if self.private_board[row][col] == "X":
            print "There is already a ship at this location!"
            return True
        return False

    def position_ship(self):
        row = self.get_coordinate("Row: ")  # check int and that it is in range (1 to ocean_size)
        col = self.get_coordinate("Col: ")
        if self.collision_check(row, col):
            print "there is already a ship at this location!"
            self.position_ship()
        else:
            print "Ship positioned at %d:%d " % (row, col)
            self.private_board[row][col] = "X"
            self.active_ships += 1

    def get_coordinate(self, prompt):
        while True:
            try:
                user_input = int(raw_input(prompt))
                if 1 <= user_input <= 5:
                    return user_input
                else:
                    print "That's not even in the ocean... Please enter a number from 1 to %s!" % overseer.ocean_size
            except ValueError:
                print "That is not a number!"

    def position_fleet(self, fleet):
        if fleet > 1:
            print "you have %d ships" % fleet
        else:
            print "you have %d ship" % fleet
        for ship in range(fleet):
            self.position_ship()

    def guess_coordinate(self, coordinate_text):
        while True:
            try:
                coordinate = int(raw_input("Guess %s: " % coordinate_text))
                if 1 <= coordinate <= overseer.ocean_size:
                    return coordinate
                else:
                    print "That's not even in the ocean..."
            except ValueError:
                print "That is not a number!"

    def check_target_location(self, row, col):  # row and col will be passed as a tuple
        if (1 > row > overseer.ocean_size) or (1 > col > overseer.ocean_size):
            print "Oops, that's not even in the ocean."
        elif self.visible_board[row][col] == "-" or self.visible_board[row][col] == "X":
                print "You guessed that one already."
        elif self.private_board[row][col] == "X":
            self.visible_board[row][col] = "X"
            print "A battleship was hit!"  # return hit?
            overseer.print_board(self.visible_board)
            self.active_ships -= 1
        else:
            print "You missed my battleship!"
            self.visible_board[row][col] = "-"


class ComputerPlayer(Player):
    def __init__(self, player_name):
        super(ComputerPlayer, self).__init__(player_name)
        self.human = False

    def position_fleet(self, fleet):
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
        if (1 > row > overseer.ocean_size) or (1 > col > overseer.ocean_size):
            print "COMPUTER: Oops, that's not even in the ocean."
        elif self.visible_board[row][col] == "-" or self.visible_board[row][col] == "X":
            print "COMPUTER: You guessed that one already."
        elif self.private_board[row][col] == "X":
            self.visible_board[row][col] = "X"
            print "COMPUTER: Congratulations! You sunk my battleship!"  # return hit?
            overseer.print_board(self.visible_board)
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
    # create a new game
    overseer.new_game(size_ocean=5, size_fleet=2, turn_max=5)

    # initialise players
    player_1 = HumanPlayer('Human')
    player_2 = ComputerPlayer('Computer')

    player_1.check_player_name()

    overseer.start_game(player_1, player_2)
    overseer.run_game(player_1, player_2)


