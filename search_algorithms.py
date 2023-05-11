import functools
import math
import random

import numpy as np

cache = functools.lru_cache(10 ** 6)
infinity = math.inf


#    ███╗   ███╗██╗███╗   ██╗      ███╗   ███╗ █████╗ ██╗  ██╗
#    ████╗ ████║██║████╗  ██║      ████╗ ████║██╔══██╗╚██╗██╔╝
#    ██╔████╔██║██║██╔██╗ ██║█████╗██╔████╔██║███████║ ╚███╔╝
#    ██║╚██╔╝██║██║██║╚██╗██║╚════╝██║╚██╔╝██║██╔══██║ ██╔██╗
#    ██║ ╚═╝ ██║██║██║ ╚████║      ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗
#    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
def minimax_search(game, state):
    """Search game tree to determine best move; return (value, move) pair."""

    player = state.to_move

    def max_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)


def minimax_search_tt(game, state):
    """Search game to determine best move; return (value, move) pair."""

    player = state.to_move

    @cache
    def max_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    @cache
    def min_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)


#     █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗       ██████╗ ███████╗████████╗ █████╗
#    ██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗      ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗
#    ███████║██║     ██████╔╝███████║███████║█████╗██████╔╝█████╗     ██║   ███████║
#    ██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║╚════╝██╔══██╗██╔══╝     ██║   ██╔══██║
#    ██║  ██║███████╗██║     ██║  ██║██║  ██║      ██████╔╝███████╗   ██║   ██║  ██║
#    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
def alphabeta_search(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)


def cache1(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}

    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]

    return wrapped


def alphabeta_search_tt(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)


def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d


def h_alphabeta_search(game, state, cutoff=cutoff_depth(3), h=lambda s, p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""
    player = state.to_move  # state è la board nel nostro caso, to_move indica il giocatore corrente

    @cache1
    def max_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity, 0)


#    ███╗   ███╗ ██████╗ ███╗   ██╗████████╗███████╗     ██████╗ █████╗ ██████╗ ██╗      ██████╗
#    ████╗ ████║██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝    ██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗
#    ██╔████╔██║██║   ██║██╔██╗ ██║   ██║   █████╗      ██║     ███████║██████╔╝██║     ██║   ██║
#    ██║╚██╔╝██║██║   ██║██║╚██╗██║   ██║   ██╔══╝      ██║     ██╔══██║██╔══██╗██║     ██║   ██║
#    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║   ██║   ███████╗    ╚██████╗██║  ██║██║  ██║███████╗╚██████╔╝
#    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝

def monte_carlo_tree_search(game, state, N=1000):
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not game.is_terminal(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state):
        """simulate the utility of current state by random picking a step"""
        player = state.to_move
        while not game.is_terminal(state):
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
        v = game.utility(state, player)
        return -v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)

    root = MCT_Node(state=state)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    return root.children.get(max_state)


class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)

