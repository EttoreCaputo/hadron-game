import sys

from hadron.game import play_game
from hadron.hadron_game import HadronGame
from hadron.hadron_graphic_module import HadronGraphicModule
from players.human import human_player

if __name__ == '__main__':
    size = 9
    game = HadronGame(size, size)

    hgm = HadronGraphicModule(size)

    game.graphic_module = hgm
    b = play_game(game,
                  {'R': human_player, 'B': human_player},
                  verbose=True)

    hgm.draw_board(b)
    print("PARTITA FINITA")
    while True:
        event = hgm.get_pygame().event.wait()
        if event.type == hgm.get_pygame().QUIT:
            sys.exit()