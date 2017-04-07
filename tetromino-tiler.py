#!/usr/bin/python3
import sys


class Tetromino:
    """Holds the possible states of a tetromino"""

    def __init__(self, shape):
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
        #self.sortkey = {'I':0, 'O':1, 'L':2, 'P':3, '2':4, '5':5, 'T':6}
        self.sortkey = {'I':6, 'O':5, 'L':4, 'P':3, '2':2, '5':1, 'T':0}
        self.rotations = shapes[shape]
        self.name = shape

    def __str__(self):
        return str(self.name)

    def __lt__(self, other):
        return self.sortkey[self.name] < other.sortkey[other.name]

    # These functions make it possible to iterate  through the rotations
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
        self.num_rows = 0
        self.num_cols = 0
        self.tetrominos = []
        self.board = []
        self.alpha = list("abcdefghijklmnopqrstuvwxyz")

    def setup(self):
        """Sets up the Board and the tetrominos"""
        for row in range(self.num_rows):
            self.board.append([])
            for col in range(self.num_cols):
                self.board[row].append('.')
        temp = self.tetrominos
        self.tetrominos = []
        for piece in temp:
            self.tetrominos.append(Tetromino(piece))
        self.tetrominos.sort()

    def tile(self):
        """Wrapper for recursive tile function, """
        # Check if the board and tetrominos have equal area
        if self.num_rows * self.num_cols != len(self.tetrominos) * 4:
            return False
        # Check if there is an even number of T tetrominos
        if self.tetrominos.count('T') % 2 != 0:
            return False
        return self.recursive_tile(0)

    def recursive_tile(self, marker):
        """recursive tile function"""
        # Check if we are done
        if self.board_is_tiled():
            return self.board
        self.display_board()
        print()
        # Get the topmost left square
        row, col = self.get_top_left()
        # Try and place each of the tetrominos
        for piece_index in range(len(self.tetrominos)):
            # If we were unable to place one type of piece here, don't try the same type
            if piece_index == 0 or self.tetrominos[piece_index] != self.tetrominos[piece_index-1]:
                # Try and place each rotation of each tetromino
                for rotation in self.tetrominos[piece_index]:
                    if not self.check(row, col, rotation):
                        pass
                    else:
                        self.mark(row, col, marker, rotation)
                        tetromino = self.tetrominos.pop(piece_index)
                        if self.useablespace():
                        # If the tetromino was successfully placed, recurse
                            self.recursive_tile(marker + 1)
                            if self.board_is_tiled():
                                return True
                        self.tetrominos.insert(piece_index, tetromino)
                        self.unmark(row, col, rotation)
                        # If none of the combinations of placements work,
        return False

    def useablespace(self):
        row = True
        useable = True
        while row and useable:
            row, col = self.get_top_left()
            count = self.mark_useable(row, col)
            if count % 4 != 0:
                useable = False
        self.unmark_useable()
        return useable

    def mark_useable(self, row, col):
        count = 0
        if self.board[row][col] == '.':
            self.board[row][col] = 'X'
            count += 1
            if(row + 1) <= self.num_rows - 1:
                count += self.mark_useable(row + 1, col)
            if(row - 1) >= 0:
                count += self.mark_useable(row - 1, col)
            if(col + 1) <= self.num_cols - 1:
                count += self.mark_useable(row, col + 1)
            if(col - 1) >= 0:
                count += self.mark_useable(row, col - 1)
        return count

    def unmark_useable(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.board[row][col] == 'X':
                    self.board[row][col] = '.'

    def unmark(self, top_left_row, top_left_col, tetromino):
        """removes the last tetromino placed"""
        for position in tetromino:
            self.board[top_left_row + position[0]][top_left_col + position[1]] = '.'

    def board_is_tiled(self):
        for row in self.board:
            for col in row:
                if col is '.':
                    return False
        return True

    def check(self, top_left_row, top_left_col, rotation):
        """Attempts to place a tetromino"""
        # Find the top leftmost position
        # Check each of the positions the tetromino takes up
        for position in rotation:

            row = top_left_row + position[0]
            col = top_left_col + position[1]
            if row > self.num_rows-1 or row < 0 or col > self.num_cols-1 or col < 0:
                return False
            if self.board[row][col] != '.':
                return False
        return True

    def mark(self, top_left_row, top_left_col, marker, tetromino):
        for position in tetromino:
            row = top_left_row + position[0]
            col = top_left_col + position[1]
            self.board[row][col] = self.alpha[marker]

    def get_top_left(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.board[row][col] == '.':
                    return row, col
        return False, False

    def display(self):
        """ To display the state of the tiler"""
        print("height:", self.num_rows)
        print("width:", self.num_cols)
        print("tetrominos to place:", self.tetrominos)

    def display_board(self):
        """To display the finished board"""
        for row in self.board:
            for col in row:
                print(' ' + col, end='')
            print()

    def main(self):
        if len(sys.argv) == 5:
            self.num_rows = int(sys.argv[1])
            self.num_cols = int(sys.argv[2])
            self.tetrominos = list(sys.argv[3])
        elif len(sys.argv) == 1:
            row_col = list(input())
            self.tetrominos = list(input())
            self.num_rows = int(row_col[0])
            self.num_cols = int(row_col[2])
        else:
            print("You entered the wrong number of arguments")
            print("Please enter height width list_of_pieces")
            return
        self.setup()
        if self.tile():
            self.display_board()
        else:
            print("It is not possible to tile this board with these tetrominos")


if __name__ == "__main__":
    import time
    if int(len(sys.argv)) == 5:
        testcount = int(sys.argv[4])
    else:
        testcount = 1
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
