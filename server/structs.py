from util import sign
from enum import Enum

MAX_COORD = 14

class Square:
    def __init__(self, fig=None, player=0):
        self.fig = fig
        self.player = player

    def empty(self):
        return self.fig is None

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if not self.is_legal():
            raise ValueError()

    def dist(self):
        return abs(self.x) + abs(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Coord(self.x * other, self.y * other)

    def __floordiv__(self, other):
        return Coord(self.x // other, self.y // other)

    def __abs__(self):
        return Coord(abs(self.x), abs(self.y))

    def dir(self):
        return Coord(sign(self.x), sign(self.y))

    def is_legal(self):
        return 0 <= self.x < MAX_COORD and 0 <= self.y < MAX_COORD

    def straight(self):
        return self.x == 0 or self.y == 0

    def diag(self):
        return self.x == self.y

class Field:
    def __init__(self, height, width):
        self.array = [[Square() for i in range(width)] for j in range(height)]

    @staticmethod
    def _getindex(index):
        if isinstance(index, Coord):
            return index
        elif isinstance(index, tuple):
            return Coord(index[0], index[1])
        raise TypeError()

    def __getitem__(self, index):
        index = Field._getindex(index)
        return self.array[index.x][index.y]

    def __setitem__(self, index, value):
        if not isinstance(value, Square):
            raise ValueError()
        index = Field._getindex(index)
        self.array[index.x][index.y] = value

Phase = Enum('Phase', "displace, move, attack, end")

class Player:
    def __init__(self, player=0):
        self.player = player

    def __not__(self):
        opponent = 2 if self.player == 1 else 1
        return Player(opponent)

    op = __not__

    def __eq__(self, other):
        if isinstance(other, int):
            return self.player == other
        return self.player == other.player

    def __bool__(self):
        return self.player != 0

FIRST = Player(1)
SECOND = Player(2)
