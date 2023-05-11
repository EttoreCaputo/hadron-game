#                                      ████████╗███████╗███████╗████████╗
#                                      ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
#                                         ██║   █████╗  ███████╗   ██║
#                                         ██║   ██╔══╝  ╚════██║   ██║
#                                         ██║   ███████╗███████║   ██║
#                                         ╚═╝   ╚══════╝╚══════╝   ╚═╝
#
#    ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗            ██╗   ██╗███████╗             █████╗ ██╗
#    ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║            ██║   ██║██╔════╝            ██╔══██╗██║
#    ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║            ██║   ██║███████╗            ███████║██║
#    ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║            ╚██╗ ██╔╝╚════██║            ██╔══██║██║
#    ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║             ╚████╔╝ ███████║            ██║  ██║██║
#    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝              ╚═══╝  ╚══════╝            ╚═╝  ╚═╝╚═╝
import sys

from players.carlo_analphabeta import carlo_analphabeta

from hadron.game import play_game
from hadron.hadron_game import HadronGame
from hadron.hadron_graphic_module import HadronGraphicModule
from players.human import human_player
from test_ai_vs_ai import heuristic_player

if __name__ == '__main__':
    size = 9
    game = HadronGame(size, size)

    hgm = HadronGraphicModule(size)

    game.graphic_module = hgm
    board = play_game(game,
                  {'R': human_player, 'B': heuristic_player(carlo_analphabeta, lambda s, p: game.simple_eval(s, p))},
                  verbose=True)

    hgm.draw_board(board)
    print("PARTITA FINITA")
    while True:
        event = hgm.get_pygame().event.wait()
        if event.type == hgm.get_pygame().QUIT:
            sys.exit()