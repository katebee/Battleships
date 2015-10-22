

class Board(object):
    def __init__(self, ocean_size):
        self.board = self._generate_empty_board(ocean_size)

    @staticmethod
    def _generate_empty_board(ocean_size):
        # this could use linked lists instead?
        board = [[" "]]
        for col in range(1, ocean_size + 1):
            board[0].append(str(col))           # Adds col numbers, also solves downstream user input vs. zero-base
        for row in range(1, ocean_size + 1):
            board.append(["O"] * ocean_size)
            board[row].insert(0, str(row))      # Adds row numbers, also solves downstream user input vs. zero-base
        return board

    def print_board(self):
        print
        for row in self.board:
            print " ".join(row)
        print