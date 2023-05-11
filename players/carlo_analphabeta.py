#     ██████╗ █████╗ ██████╗ ██╗      ██████╗
#    ██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗
#    ██║     ███████║██████╔╝██║     ██║   ██║
#    ██║     ██╔══██║██╔══██╗██║     ██║   ██║
#    ╚██████╗██║  ██║██║  ██║███████╗╚██████╔╝
#     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝
#     █████╗ ███╗   ██╗ █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗ ██████╗ ███████╗████████╗ █████╗
#    ██╔══██╗████╗  ██║██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗
#    ███████║██╔██╗ ██║███████║██║     ██████╔╝███████║███████║██████╔╝█████╗     ██║   ███████║
#    ██╔══██║██║╚██╗██║██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║██╔══██╗██╔══╝     ██║   ██╔══██║
#    ██║  ██║██║ ╚████║██║  ██║███████╗██║     ██║  ██║██║  ██║██████╔╝███████╗   ██║   ██║  ██║
#    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
import math
import random
import time

import numpy as np

infinity = math.inf


def carlo_analphabeta(game, state, h=lambda s, p: 0, timeout=3000):
    start_time = get_millis()
    if len(game.actions(state)) > 6:
        return 0, monte_carlo_tree_search_timed(game, state, start_time, time_limit=timeout - 100)
    else:
        return h_alphabeta_search_timed(game, state, start_time, cutoff=cutoff_depth_time(12, timeout - 100), h=h)


#    ██╗  ██╗     █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗ ██████╗ ███████╗████████╗ █████╗
#    ██║  ██║    ██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗
#    ███████║    ███████║██║     ██████╔╝███████║███████║██████╔╝█████╗     ██║   ███████║
#    ██╔══██║    ██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║██╔══██╗██╔══╝     ██║   ██╔══██║
#    ██║  ██║    ██║  ██║███████╗██║     ██║  ██║██║  ██║██████╔╝███████╗   ██║   ██║  ██║
#    ╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝

def cache_h_alphabeta(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}

    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]

    return wrapped


def get_millis():
    return round(time.time() * 1000)


def cutoff_depth_time(max_depth, time_limit):
    return lambda game, state, start_time, current_time, depth: \
        depth > max_depth \
        or current_time - start_time > time_limit


def h_alphabeta_search_timed(game, state, start_time, cutoff=cutoff_depth_time(6, 2000), h=lambda s, p: 0):
    player = state.to_move

    @cache_h_alphabeta
    def max_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, start_time, get_millis(), depth):
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

    @cache_h_alphabeta
    def min_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, start_time, get_millis(), depth):
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

    v, move = max_value(state, -infinity, +infinity, 0)
    return v, move


#    ███╗   ███╗ ██████╗ ███╗   ██╗████████╗███████╗     ██████╗ █████╗ ██████╗ ██╗      ██████╗
#    ████╗ ████║██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝    ██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗
#    ██╔████╔██║██║   ██║██╔██╗ ██║   ██║   █████╗      ██║     ███████║██████╔╝██║     ██║   ██║
#    ██║╚██╔╝██║██║   ██║██║╚██╗██║   ██║   ██╔══╝      ██║     ██╔══██║██╔══██╗██║     ██║   ██║
#    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║   ██║   ███████╗    ╚██████╗██║  ██║██║  ██║███████╗╚██████╔╝
#    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝
class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)


def monte_carlo_tree_search_timed(game, state, start_time, time_limit):
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

    num_iteration = 0
    while get_millis() - start_time < time_limit:
        num_iteration += 1
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    return root.children.get(max_state)
