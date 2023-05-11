import os
import random
from collections import deque

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam


class Agent:
    def __init__(self, state_size, action_size, weights_file="hadron_weight.h5"):
        self.weight_backup = weights_file
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.learning_rate = 0.001
        self.gamma = 0.95   # 0.95
        self.exploration_rate = 1.0
        self.exploration_min = 0.01
        self.exploration_decay = 0.985 #0.995
        self.brain = self._build_model()
        self.loss_history = []

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim= self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))

        if os.path.isfile(self.weight_backup):
            model.load_weights(self.weight_backup)
            self.exploration_rate = self.exploration_min
        return model

    def save_model(self):
        #self.brain.save(self.weight_backup)
        print("SALVATAGGIO NON ATTIVO")

    def act(self, state, env):
        if np.random.rand() <= self.exploration_rate:
            (r, c) = random.choice(env.actions(env.board))
            return (r * round(self.state_size ** 0.5)) + c
        act_values = self.brain.predict(state.reshape([1, -1])[0], verbose=0)
        return np.argmax(act_values[0])

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, sample_batch_size):
        if len(self.memory) < sample_batch_size:
            return
        sample_batch = random.sample(self.memory, sample_batch_size)
        for state, action, reward, next_state, done in sample_batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.brain.predict(next_state.reshape([1, -1]), verbose=0)[0])

            target_f = self.brain.predict(state.reshape([1, -1])[0], verbose=0)
            target_f[0][action] = target
            history = self.brain.fit(state.reshape([1, -1])[0], target_f, epochs=1, verbose=0)
            self.loss_history.append(history.history['loss'])
        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay