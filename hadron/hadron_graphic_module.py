import pygame

from hadron.board import Board


class HadronGraphicModule:
    # Definizione di costanti per i colori
    BLACK = (30, 30, 30)
    WHITE = (255, 255, 255)
    LIGHT_LIGHT_GRAY = (240, 240, 240)
    LIGHT_GRAY = (222, 222, 222)
    GRAY = (200, 200, 200)
    RED = (202, 70, 55)
    BLUE = (90, 96, 152)

    def __init__(self, size, to_move='R'):
        # Definizione di costanti per le dimensioni della griglia
        self.board_size = size
        self.cell_size = 48
        self.cell_spacing = 4
        self.board_margin = 10
        self.cell_width_edge = 1

        # Definizione della finestra di gioco
        self.dim = self.cell_size * self.board_size + self.board_margin * 2 + self.cell_spacing * (self.board_size - 1)
        self.window_size = (self.dim, self.dim)

        # Inizializzazione della libreria pygame
        pygame.init()

        # Definizione della finestra di gioco
        pygame.display.set_caption("Hadron")
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self.LIGHT_GRAY)

        # Definisci una variabile per tenere traccia di chi è il turno
        self.current_player = to_move

        # Definizione delle posizioni dei simboli
        self.cell_positions = [
            [
                (
                    (i * self.cell_size + self.board_margin) + (i * self.cell_spacing),
                    (j * self.cell_size + self.board_margin) + (j * self.cell_spacing)
                ) for j in range(self.board_size)
            ] for i in range(self.board_size)
        ]

    # Definizione della funzione per disegnare la griglia
    def draw_board(self, board: Board) -> pygame:
        assert board.height == self.board_size
        for i in range(self.board_size):
            for j in range(self.board_size):
                color = self.LIGHT_LIGHT_GRAY
                width = self.cell_width_edge
                match board[i, j]:
                    case 'R':
                        color = self.RED
                        width = 0
                    case 'B':
                        color = self.BLUE
                        width = 0

                if width != 0:
                    pygame.draw.rect(
                        surface=self.screen,
                        color=self.GRAY,
                        rect=(
                            (j * self.cell_size + self.board_margin) + (j * self.cell_spacing),
                            (i * self.cell_size + self.board_margin) + (i * self.cell_spacing),
                            self.cell_size,
                            self.cell_size
                        ),
                        border_radius=10,
                        width=self.cell_width_edge
                    )

                pygame.draw.rect(
                    surface=self.screen,
                    color=color,
                    rect=(
                        (j * self.cell_size + self.board_margin) + (j * self.cell_spacing) + width,
                        (i * self.cell_size + self.board_margin) + (i * self.cell_spacing) + width,
                        self.cell_size - width * 2,
                        self.cell_size - width * 2
                    ),
                    border_radius=10,
                    width=0
                )

        pygame.display.update()
        return pygame


    def get_pygame(self):
        return pygame

    # Definizione della funzione per determinare la cella selezionata
    def get_cell(self, pos):
        x, y = pos
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.cell_positions[i][j][1] <= x <= self.cell_positions[i][j][1] + self.cell_size \
                        and self.cell_positions[i][j][0] <= y <= self.cell_positions[i][j][0] + self.cell_size:
                    return i, j
        return -1, -1
