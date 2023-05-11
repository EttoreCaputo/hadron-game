import random


def random_player(game, state):
    return random.choice(list(game.actions(state)))