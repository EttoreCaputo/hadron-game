from collections import defaultdict

import numpy as np


class Board(defaultdict):
    """A board has the player to move, a cached utility value,
    and a dict of {(x, y): player} entries."""
    empty = '.'
    off = '#'
    R_PLAYER = 'R'
    B_PLAYER = 'B'

    def __init__(self, width=7, height=7, to_move=None, **kwds):
        super().__init__()
        self.to_move = to_move
        self.width = width
        self.height = height
        self.utility = 0
        self.__dict__.update(width=width, height=height, to_move=to_move, **kwds)

    def new(self, changes: dict, **kwds) -> 'Board':
        """Given a dict of {(x, y): contents} changes, return a new BoardProf with the changes."""
        board = Board(width=self.width, height=self.height, **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off

    def __hash__(self):
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)

    def __repr__(self):
        def row(x): return ' '.join(self[x, y] for y in range(self.width))

        return '\n'.join(map(row, range(self.height))) + '\n'

    def __reduce__(self):
        return self.__class__, (self.width, self.height, self.to_move), None, None, iter(self.items())

    def to_matrix(self):
        array = []

        def row(x): return [self.__transform(self[x, y]) for y in range(self.width)]

        for r in range(self.height):
            array.append(row(r))
        return np.matrix(array)

    def __transform(self, c):
        if c == self.empty:
            return 0
        if c == 'R':
            return 1
        return -1
