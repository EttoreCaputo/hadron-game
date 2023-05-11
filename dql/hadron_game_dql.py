import matplotlib.pyplot as plt
from PIL import Image

from hadron.board import Board
from hadron.hadron_game import HadronGame


#from hadron.hadron_graphic_module import HadronGraphicModule


class HadronGameDQL(HadronGame):

    def __init__(self, size=9):
        self.REWARD_BAD_MOVE = -15
        self.REWARD_GOOD_MOVE = 0
        self.REWARD_WIN = 10
        self.REWARD_LOSE = -10
        super().__init__(size, size)
        self.size = size
        self.board = self.initial
        #self.graphic_module = HadronGraphicModule(size)

    def reset(self):
        self.board = Board(width=self.size, height=self.size, to_move='R', utility=0)
        # self.graphic_module.screen.fill(color=self.graphic_module.GRAY)
        return self.board.to_matrix()

    def step(self, action):

        """
            Il parametro action é un intero che puó assumere i valori da 0 a 80.
             - indica la cella su cui un determinato agente effettua la mossa
        """
        player = self.board.to_move

        move = (action // self.size, action % self.size)

        new_board = self.result(self.board, move)
        self.board = new_board

        win = self.check_winner(self.board)

        remaining_moves = len(self.actions(self.board))

        if not win:
            if player == 'R' and remaining_moves % 2 == 0 \
                    or player == 'B' and remaining_moves % 2 == 1:
                reward = self.REWARD_BAD_MOVE
            else:
                reward = self.REWARD_GOOD_MOVE
        else:
            if player == 'B':
                reward = self.REWARD_LOSE
            else:
                reward = self.REWARD_WIN

        return self.board.to_matrix(), reward, win

    def render(self):
        self.graphic_module.draw_board(self.board)
        #finish = False
        #while not finish:
        #    event = self.graphic_module.get_pygame().event.wait()
        #    if event.type == self.graphic_module.get_pygame().QUIT:
        #        finish = True

    def plot_board(self):
        self.graphic_module.draw_board(self.board)
        pygame = self.graphic_module.get_pygame()
        screen = self.graphic_module.screen
        pygame.image.save(screen, "screenshot.jpg")

        plt.imshow(Image.open('screenshot.jpg'))
        plt.show()
