#!/usr/bin/python3
import sys


class Tetromino:
    """Holds the possible states of a tetromino"""
    rotations = []
    name = ''

    def __init__(self, shape):
        shapes = {'I': [[(0, 0), (1, 0), (2, 0), (3, 0)],
                        [(0, 0), (0, 1), (0, 2), (0, 3)]],

                  'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]],

                  'L': [[(0, 0), (1, 0), (2, 0), (2, 1)],
                        [(0, 0), (1, 0), (0, 1), (0, 2)],
                        [(0, 0), (0, 1), (1, 1), (2, 1)],
                        [(0, 0), (1, -2), (1, -1), (1, 0)]],

                  'P': [[(0, 0), (0, 1), (1, 0), (2, 0)],
                        [(0, 0), (1, 2), (0, 1), (0, 2)],
                        [(0, 0), (1, 0), (2, 0), (2, -1)],
                        [(0, 0), (1, 0), (1, 1), (1, 2)]],

                  'Z': [[(0, 0), (0, 1), (1, 1), (1, 2)],
                        [(0, 0), (0, 1), (-1, 1), (2, -1)]],

                  'S': [[(0, 0), (0, 1), (1, -1), (1, 0)],
                        [(0, 0), (1, 0), (1, 1), (2, 1)]],

                  'T': [[(0, 0), (0, 1), (0, 2), (1, 1)],
                        [(0, 0), (1, 0), (2, 0), (1, -1)],
                        [(0, 0), (1, -1), (1, 0), (1, 1)],
                        [(0, 0), (1, 0), (2, 0), (1, 1)]]
                  }
        self.rotations = shapes[shape]
        self.name = shape


class Tiler:
    """This is to take a board and set of Tetrominos to see if that board is tileable"""

    height = 0
    width = 0
    tetrominos = []
    board = []
    numI = 0
    numO = 0
    numL = 0
    numP = 0
    numZ = 0
    numS = 0
    numT = 0

    def __init__(self):
        self.height = 0
        self.width = 0
        self.tetrominos = []
        self.board = []
        self.numI = 0
        self.numO = 0
        self.numL = 0
        self.numP = 0
        self.numZ = 0
        self.numS = 0
        self.numT = 0

    def setup(self):
        """Sets up the Board and the tetrominos"""
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append('X')
        temp = Tetromino('I')
        for i in range(self.numI):
            self.tetrominos.append(temp)
        temp = Tetromino('O')
        for i in range(self.numO):
            self.tetrominos.append(temp)
        temp = Tetromino('L')
        for i in range(self.numL):
            self.tetrominos.append(temp)
        temp = Tetromino('P')
        for i in range(self.numP):
            self.tetrominos.append(temp)
        temp = Tetromino('Z')
        for i in range(self.numZ):
            self.tetrominos.append(temp)
        temp = Tetromino('S')
        for i in range(self.numS):
            self.tetrominos.append(temp)
        temp = Tetromino('T')
        for i in range(self.numT):
            self.tetrominos.append(temp)

    def tile(self):
        """Wrapper for recursive tile function, """
        # Check if the board and tetrominos have equal area
        if self.height * self.width != len(self.tetrominos) * 4:
            return False
        # Check if there is an even number of T tetrominos
        if self.tetrominos.count('T') % 2 != 0:
            return False
        return self.recursive_tile(self.board)

    def recursive_tile(self, tetrominos, board):
        """recursive tile function"""
        # Check if we are done
        if self.board_is_tiled(board):
            return True
        # Try and place each of the tetrominos
        for tetromino in tetrominos:
            # Try and place each rotation of each tetromino
            for rotation in tetromino:
                # If the tetromino was successfully placed, recurse
                if self.place(rotation, board):
                    tetrominos.remove(tetromino)
                    self.recursive_tile(tetrominos, board)
        # If none of the combinations of placements work,
        return False

    def board_is_tiled(self, board):
        for row in board:
            for col in row:
                if col is 'X':
                    return False
        self.board = board
        return True

    #def place

    def display(self):
        """ To display the state of the tiler"""
        print("height:", self.height)
        print("witdh:", self.height)
        print("tetrominos to place:", self.tetrominos)

    def display_board(self):
        """To display the finished board"""
        for row in self.board:
            for col in row:
                print(' ' + col + ' ', end='')
            print()

    def main(self):
        if len(sys.argv) == 10:
            self.height = int(sys.argv[1])
            self.width = int(sys.argv[2])
            self.numI = int(sys.argv[3])
            self.numO = int(sys.argv[4])
            self.numL = int(sys.argv[5])
            self.numP = int(sys.argv[6])
            self.numZ = int(sys.argv[7])
            self.numS = int(sys.argv[8])
            self.numT = int(sys.argv[9])
        elif len(sys.argv) == 1:
            print("Welcome to the Tetronimo tiler")
            self.height = int(input("Please enter the height of the board: "))
            self.width = int(input("Please enter the width of the board: "))
            self.numI = int(input("Please enter the number of I Tetrominos: "))
            self.numO = int(input("Please enter the number of O Tetrominos: "))
            self.numL = int(input("Please enter the number of L Tetrominos: "))
            self.numP = int(input("Please enter the number of P Tetrominos: "))
            self.numZ = int(input("Please enter the number of Z Tetrominos: "))
            self.numS = int(input("Please enter the number of S Tetrominos: "))
            self.numT = int(input("Please enter the number of T Tetrominos: "))
        else:
            print("You entered the wrong number of arguments")
            print("Please enter height width I O L P Z S T")
            return
        #self.display()
        self.setup()
        self.display_board()
        if self.tile():
            self.display_board()
        else:
            print("It is not possible to tile this board with these tetrominos")


if __name__ == "__main__":
    tiler = Tiler()
    tiler.main()
