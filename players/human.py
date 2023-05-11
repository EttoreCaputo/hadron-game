import sys

from pygame.locals import QUIT, MOUSEBUTTONUP


def human_player(game, state):
    i = j = 0
    game.graphic_module.draw_board(state)
    pygame = game.graphic_module.get_pygame()
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(QUIT)
    pygame.event.set_allowed(MOUSEBUTTONUP)
    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            i, j = game.graphic_module.get_cell(pos)
            if (i, j) in game.actions(state):
                running = False
    return i, j
