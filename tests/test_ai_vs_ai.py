#                  ████████╗███████╗███████╗████████╗
#                  ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
#                     ██║   █████╗  ███████╗   ██║
#                     ██║   ██╔══╝  ╚════██║   ██║
#                     ██║   ███████╗███████║   ██║
#                     ╚═╝   ╚══════╝╚══════╝   ╚═╝
#
#     █████╗ ██╗            ██╗   ██╗███████╗             █████╗ ██╗
#    ██╔══██╗██║            ██║   ██║██╔════╝            ██╔══██╗██║
#    ███████║██║            ██║   ██║███████╗            ███████║██║
#    ██╔══██║██║            ╚██╗ ██╔╝╚════██║            ██╔══██║██║
#    ██║  ██║██║             ╚████╔╝ ███████║            ██║  ██║██║
#    ╚═╝  ╚═╝╚═╝              ╚═══╝  ╚══════╝            ╚═╝  ╚═╝╚═╝
import time


from hadron.board import Board
from hadron.game import play_game_thread
from hadron.hadron_game import HadronGame
from players.carlo_analphabeta import carlo_analphabeta
from players.monte_carlo import monte_carlo


def get_millis():
    return round(time.time() * 1000)


def test(r_player, b_player, rep, verbose, dim=9):
    # random.seed()
    blue_wins = red_wins = 0
    average_time = 0

    for i in range(rep):
        start = get_millis()
        game = HadronGame(dim, dim)
        board: Board = play_game_thread(game, {'R': r_player(game), 'B': b_player(game)}, verbose=verbose)
        end = get_millis()
        average_time += (end - start)

        if board.to_move == 'B':
            red_wins += 1
        else:
            blue_wins += 1

        print('\r[', end="")
        print('+' * red_wins, end="")
        print('*' * blue_wins, end="")
        print(' ' * (rep - (i + 1)), end="")
        print(']', end="", flush=True)

    tot = red_wins + blue_wins
    print("\tRED:", red_wins / float(tot), "\tBLUE:", blue_wins / float(tot), "\tTIME:", average_time / float(rep),
          "ms")


def heuristic_player(search_algorithm, heuristic=lambda s, p: 0.0):
    return lambda game, state: search_algorithm(game, state, h=heuristic)[1]


def player(search_algorithm):
    return lambda game, state: search_algorithm(game, state)[1]


if __name__ == '__main__':
    size = 9
    game = HadronGame(size, size)
    rep = 20

    print("\n\n------   carlo_analphabeta(+) - monte_carlo(*)   ------")
    test(
        r_player=lambda g: heuristic_player(carlo_analphabeta, lambda s, p: g.simple_eval(s, p)),
        b_player=lambda _: player(monte_carlo),
        rep=rep,
        verbose=False,
        dim=size
    )

    print("\n\n------   carlo_analphabeta(+) - monte_carlo(*)   ------")
    test(
        r_player=lambda _: player(monte_carlo),
        b_player=lambda g: heuristic_player(carlo_analphabeta, lambda s, p: g.simple_eval(s, p)),
        rep=rep,
        verbose=False,
        dim=size
    )
