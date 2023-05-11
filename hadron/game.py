import random
import threading
import time


class Game:
    """A game is similar to a problem, but it has a terminal test instead of
    a goal test, and a utility for each terminal state. To create a game,
    subclass this class and implement `actions`, `result`, `is_terminal`,
    and `utility`. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError


def get_millis():
    return round(time.time() * 1000)


def play_game(game, strategies: dict, verbose=False):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move."""

    state = game.initial
    while not game.is_terminal(state):
        start = get_millis()

        player = state.to_move
        move = strategies[player](game, state)
        state = game.result(state, move)

        end = get_millis()

        if verbose:
            print('Player', player, '\tmove:', move, '\ttime:', (end - start), 'ms')
            print(state)
    return state


def player_move(player, state, strategies, game, move):
    move.append(strategies[player](game, state))


def play_game_thread(game, strategies: dict, verbose=False):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move."""

    state = game.initial
    while not game.is_terminal(state):
        start = get_millis()

        trouble = False
        available_moves = list(game.actions(state))
        move = []

        player = state.to_move

        th_player = threading.Thread(target=player_move, args=(player, state, strategies, game, move))
        th_player.start()

        # attende per al piú tre secondi
        th_player.join(3)

        # se il thread é ancora in esecuzione, imposta la variabile trouble a True
        # questo indica che il giocatore ha superato il tempo limite
        if th_player.is_alive() or move[0] not in available_moves:
            trouble = True

        # gestione di eventuali problemi dovuti al timeout o a mosse non valide
        if trouble:
            print("Timeout, random choice for player ", player)
            move_in_trouble = random.choice(list(game.actions(state)))
            state = game.result(state, move_in_trouble)
        else:
            state = game.result(state, move[0])

        end = get_millis()
        if verbose:
            print('Player', player, '\tmove:', move, '\ttime:', (end - start), 'ms')
            print(state)
    return state


def play_game_process(game, parent_connX, parent_connO, verbose=False, timeout=3):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move."""


    """
        A main that use this method should be like this:
        
        game = Hadron()
        parent_connX, child_connX = multiprocessing.Pipe()
        parent_connO, child_connO = multiprocessing.Pipe()
        qX = multiprocessing.Queue()
        playerX = multiprocessing.Process(target=playerXmodule.playerStrategy, args=(child_connX, game, qX))
        qO = multiprocessing.Queue()
        playerO = multiprocessing.Process(target=playerOmodule.playerStrategy, args=(child_connO, game, qO))

        playerX.start()
        playerO.start()

        time.sleep(1)
        print(game.utility(play_game(game, playerX, playerO, verbose=False), 'X'))

        parent_connX.close()
        child_connX.close()
        parent_connO.close()
        child_connO.close()

        playerX.kill()
        playerO.kill()
        
    """


    state = game.initial
    number_of_move = 0
    move = (0, 0)
    number_of_movePl = 0

    while not game.is_terminal(state):
        player = state.to_move
        number_of_move += 1
        available_moves = list(game.actions(state))
        trouble = False

        if player == 'X':
            parent_connX.send((number_of_move, state))
            if parent_connX.poll(timeout):
                (number_of_movePl, state_recv, move) = parent_connX.recv()
            else:
                trouble = True
                print("Timeout, random choice for player X")
        else:
            parent_connO.send((number_of_move, state))
            if parent_connO.poll(timeout):
                (number_of_movePl, state_recv, move) = parent_connO.recv()
            else:
                trouble = True
                print("Timeout, random choice for player O")

        # further check to avoid syncronization troubles
        if number_of_movePl != number_of_move:
            trouble = True
            print("Different number of move, random choice for player ", player)
            # further check to avoid wrong moves
        elif move not in available_moves:
            print("choices for ", player, available_moves, " move number", number_of_move)
            print("Wrong move", move, ", using random choice for player ", player)

            trouble = True

        if trouble:  # something went wrong and we perform a random move
            move = random.choice(available_moves)
            # we send to the player the information that the move number_of_move is not needed anymore
            if player == 'X':
                parent_connX.send((number_of_move, None))
            else:
                parent_connO.send((number_of_move, None))

        # move = strategies[player](game, state)
        state = game.result(state, move)
        if verbose:
            print('Player', player, 'move: (', move[1] + 1, ',', move[0] + 1, ')')
            print(state)
            if game.is_terminal(state):
                print("Result for player yellow (X): ", game.utility(state, 'X'))
        # draw_board(state)

    # Send the final state to the players
    parent_connX.send((-1, state))
    parent_connO.send((-1, state))

    return state
