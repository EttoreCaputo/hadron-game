import numpy as np
from matplotlib import pyplot as plt

from dql.agents import Agent
from dql.hadron_game_dql import HadronGameDQL
from players.random import random_player


class AgentTrainer:
    def __init__(self, size, env, agent, player):
        self.sample_batch_size = 256
        self.episodes = 100
        self.env = env
        self.size = size
        self.agent = agent
        self.adv_player = player

    def run(self):
        blue_wins = red_wins = 0
        try:
            for index_episode in range(self.episodes):
                state = self.env.reset()

                done = False
                while not done:
                    # self.env.render()

                    # mossa dell'agente
                    action = self.agent.act(state, self.env)
                    next_state, reward, done = self.env.step(action)

                    # self.env.plot_board()
                    # time.sleep(1)

                    if not done:
                        # mossa del player avversario
                        (r, c) = self.adv_player(self.env, self.env.board)
                        action_adv = (r * self.size) + c
                        next_state, reward, done = self.env.step(action_adv)

                        # self.env.plot_board()
                        # time.sleep(1)

                    # salvo
                    self.agent.remember(state, action, reward, next_state, done)
                    state = next_state

                if (index_episode+1) % 5 == 0 and len(self.agent.memory) > self.sample_batch_size:
                    y = np.array(self.agent.loss_history)
                    x = np.array(range(len(self.agent.loss_history)))

                    coef = np.polyfit(x, np.squeeze(y), 1)
                    poly1d_fn = np.poly1d(coef)
                    plt.plot(x, y, 'o', color="lightgray", alpha=.2)
                    plt.plot(x, poly1d_fn(x), '--', color="black", alpha=.2)

                    plt.show()

                if self.env.board.to_move == 'B':
                    winner = "R"
                    red_wins += 1
                else:
                    winner = "B"
                    blue_wins += 1

                print(
                    "Episode {}     "
                    "Winner: {}     "
                    "Partial result: r_{}-b_{}     "
                    "Exploration_rate: {}"
                    .format(index_episode+1, winner, red_wins, blue_wins, self.agent.exploration_rate))

                self.agent.replay(self.sample_batch_size)
        finally:
            print("R:", red_wins, "B:", blue_wins)
            self.agent.save_model()


if __name__ == "__main__":
    dim = 9
    file_name = "hadron_weight_ep300-bat64-dense64-dense64.h5"
    hdql = AgentTrainer(
        dim,
        HadronGameDQL(dim),
        Agent(dim ** 2, dim ** 2, file_name),
        random_player
    )
    hdql.run()
