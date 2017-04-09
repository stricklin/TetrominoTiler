#!/usr/bin/python3
import sys


class Tetromino:
    """Holds the possible states of a tetromino"""

    def __init__(self, shape):
        """Will make a list of rotations of a tetromino from a char"""
        shapes = {'I': [[(0, 0), (0, 1), (0, 2), (0, 3)],
                        [(0, 0), (1, 0), (2, 0), (3, 0)]],

                  'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]],

                  'L': [[(0, 0), (1, 0), (0, 1), (0, 2)],
                        [(0, 0), (0, 1), (1, 1), (2, 1)],
                        [(0, 0), (1, -2), (1, -1), (1, 0)],
                        [(0, 0), (1, 0), (2, 0), (2, 1)]],

                  'P': [[(0, 0), (1, 2), (0, 1), (0, 2)],
                        [(0, 0), (0, 1), (1, 0), (2, 0)],
                        [(0, 0), (1, 0), (2, 0), (2, -1)],
                        [(0, 0), (1, 0), (1, 1), (1, 2)]],

                  '2': [[(0, 0), (0, 1), (1, 1), (1, 2)],
                        [(0, 0), (1, 0), (1, -1), (2, -1)]],

                  '5': [[(0, 0), (0, 1), (1, -1), (1, 0)],
                        [(0, 0), (1, 0), (1, 1), (2, 1)]],

                  'T': [[(0, 0), (0, 1), (0, 2), (1, 1)],
                        [(0, 0), (1, 0), (2, 0), (1, -1)],
                        [(0, 0), (1, -1), (1, 0), (1, 1)],
                        [(0, 0), (1, 0), (2, 0), (1, 1)]]
                  }
        # The sortkey is the order of how I want the tetrominos placed
        # After some testing, it seems like it's best to try and place simple shapes first
        self.sortkey = {'I': 0, 'O': 1, 'L': 2, 'P': 3, '2': 4, '5': 5, 'T': 6}
        self.rotations = shapes[shape]
        self.name = shape

    def __str__(self):
        return str(self.name)

    def __lt__(self, other):
        """This allows the sort() function to be called on a list of tetrominos"""
        return self.sortkey[self.name] < other.sortkey[other.name]

    # iter and next make it possible to iterate through the rotations
    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        if self.current > len(self.rotations)-1:
            raise StopIteration
        to_return = self.rotations[self.current]
        self.current += 1
        return to_return


class Tiler:
    """This is to take a board and set of Tetrominos to see if that board is tileable"""

    def __init__(self):
        self.vertical = 0
        self.horizontal = 0
        self.tetrominos = []
        self.board = []
        self.alpha = list("abcdefghijklmnopqrstuvwxyz")

    def setup(self):
        """Sets up the Board and the tetrominos"""
        # Initialize the board
        for k in range(self.vertical):
            self.board.append([])
            for j in range(self.horizontal):
                self.board[k].append('.')

        # Take the list of letters, turn them into tetrominos, and sort them
        temp = self.tetrominos
        self.tetrominos = []
        for piece in temp:
            self.tetrominos.append(Tetromino(piece))
        self.tetrominos.sort()

    def tile(self):
        """Wrapper for recursive tile function"""
        # Check if the board and tetrominos have equal area
        if self.vertical * self.horizontal != len(self.tetrominos) * 4:
            return False
        # Check if there is an even number of T tetrominos
        if self.tetrominos.count('T') % 2 != 0:
            return False
        return self.recursive_tile(0, self.tetrominos, self.board)

    def recursive_tile(self, marker, tetrominos, board):
        """recursive tile function"""
        # Check if we are done
        if self.board_is_tiled(board):
            return board
        
        # Get the topmost left square
        row, col = self.get_top_left(board)

        # Try and place each of the tetrominos
        for piece_index in range(len(tetrominos)):

            if piece_index == 0 or tetrominos[piece_index] != tetrominos[piece_index-1]:
                # Try and place each rotation of each tetromino
                for rotation in tetrominos[piece_index]:
                    # If the tetromino was successfully placed, recurse
                    if not self.check(row, col, marker, rotation, board):
                        pass
                    else:
                        self.mark(row, col, marker, rotation, board)
                        tetromino = tetrominos.pop(piece_index)
                        result = self.recursive_tile(marker + 1, tetrominos, board)
                        if self.board_is_tiled(result):
                            return result
                        tetrominos.insert(piece_index, tetromino)
                        self.unmark(row, col, rotation, board)
                        # If none of the combinations of placements work,
        return False

    def unmark(self, top_left_row, top_left_col, tetromino, board):
        """removes the last tetromino placed"""
        for position in tetromino:
            board[top_left_row + position[0]][top_left_col + position[1]] = '.'

    def board_is_tiled(self, board):
        if not board:
            return False
        for row in board:
            for col in row:
                if col is '.':
                    return False
        return True

    def check(self, top_left_row, top_left_col, marker, tetromino, board):
        """Attempts to place a tetromino"""
        # Find the top leftmost position
        # Check each of the positions the tetromino takes up
        for position in tetromino:

            row = top_left_row + position[0]
            col = top_left_col + position[1]
            if row > self.vertical-1 or row < 0 or col > self.horizontal-1 or col < 0:
                return False
            if board[row][col] != '.':
                return False
        return True

    def mark(self, top_left_row, top_left_col, marker, tetromino, board):
        for position in tetromino:
            board[top_left_row + position[0]][top_left_col + position[1]] = self.alpha[marker]

    def get_top_left(self, board):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == '.':
                    return row, col
        return False, False

    def display(self):
        """ To display the state of the tiler"""
        print("height:", self.vertical)
        print("width:", self.horizontal)
        print("tetrominos to place:", self.tetrominos)

    def display_board(self):
        """To display the finished board"""
        for row in self.board:
            for col in row:
                print(' ' + col, end='')
            print()

    def main(self):
        if len(sys.argv) == 5:
            self.vertical = int(sys.argv[1])
            self.horizontal = int(sys.argv[2])
            self.tetrominos = list(sys.argv[3])
        elif len(sys.argv) == 1:
            hort_vert = input().split(' ')
            self.tetrominos = list(input())
            self.horizontal = int(hort_vert[0])
            self.vertical = int(hort_vert[1])
        else:
            print("You entered the wrong number of arguments")
            print("Please enter height width list_of_pieces number_of_tests")
            return
        self.setup()
        if self.tile():
            self.display_board()
        else:
            print("?")


if __name__ == "__main__":
    import time
    if int(len(sys.argv)) == 5:
        testcount = int(sys.argv[4])
        total = 0
        for i in range(testcount):
            start = time.time()
            tiler = Tiler()
            tiler.main()
            end = time.time()
            total += end - start
            print("Time: ", end - start)
        avgtime = total/testcount
        print("Average time: ", avgtime)
    else:
        tiler = Tiler()
        tiler.main()

