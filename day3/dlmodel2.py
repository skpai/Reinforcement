import numpy as np
from collections import deque
from maze import *

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,  Flatten
from tensorflow.keras.optimizers import Adam
import random

from datetime import datetime

class Agent:
    def __init__(self, maze, episodes, times):
        self.maze=maze
        self.episodes=episodes
        self.times=times

    
class NeuralNetworkSolver:
    def __init__(self, state_size, action_size):
        self.state_size = state_size # list size of state
        self.action_size = action_size # list size of action
        self.memory = deque(maxlen=100000) # memory space
        self.gamma = 0.9 # discount rate
        self.epsilon = 1.0 # randomness of choosing random action or the best one
        self.e_decay = 0.9999 # epsilon decay rate
        self.e_min = 0.01 # minimum rate of epsilon
        self.learning_rate = 0.0001 # learning rate of neural network
        self.model = self.build_model() # model
        self.model.summary() # model summary

    # model for neural network
    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=(2,2), activation='relu'))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss="mse", optimizer=Adam())
        return model

    # remember state, action, its reward, next state and next possible action. done means boolean for goal
    def remember_memory(self, state, action, reward, next_state, next_movables, done):
        self.memory.append((state, action, reward, next_state, next_movables, done))

    # choosing action depending on epsilon
    def choose_action(self, state, movables):
        if self.epsilon >= random.random():
            # randomly choosing action
            return random.choice(movables)
        else:
            # choosing the best action from model.predict()
            return self.choose_best_action(state, movables)
        
    # choose the best action to maximize reward expectation
    def choose_best_action(self, state, movables):
        best_actions = []
        max_act_value = -100
        for a in movables:
            np_action = np.array([[state, a]])
            act_value = self.model.predict(np_action)
            if act_value > max_act_value:
                best_actions = [a,]
                max_act_value = act_value
            elif act_value == max_act_value:
                best_actions.append(a)
        return random.choice(best_actions)

    # this experience replay is going to train the model from memorized states, actions and rewards
    def replay_experience(self, batch_size):
        batch_size = min(batch_size, len(self.memory))
        minibatch = random.sample(self.memory, batch_size)
        X = []
        Y = []
        for i in range(batch_size):
            state, action, reward, next_state, next_movables, done = minibatch[i]
            input_action = [state, action]
            if done:
                target_f = reward
            else:
                next_rewards = []
                for i in next_movables:
                    np_next_s_a = np.array([[next_state, i]])
                    next_rewards.append(self.model.predict(np_next_s_a))
                np_n_r_max = np.amax(np.array(next_rewards))
                target_f = reward + self.gamma * np_n_r_max
            X.append(input_action)
            Y.append(target_f)
        np_X = np.array(X)
        np_Y = np.array([Y]).T
        self.model.fit(np_X, np_Y, epochs=1, verbose=0)
        if self.epsilon > self.e_min:
            self.epsilon *= self.e_decay

def main():
    ACTIONS = ['up', 'down', 'left', 'right']
    initSTATE = (0,0)
    SIZE = (5,5) # maze size
    episodes = 2000

    # number of times to sample the combination of state, action and reward
    times = 1000

    target = [(3,1), (4,4)]
    t_reward = 100
    f_reward_list = -1+np.zeros(SIZE)
    maze = Maze(ACTIONS)
    maze.build_map(SIZE, target, t_reward)
    agent = Agent(maze,episodes= episodes, times= times)
    state_size = 2
    action_size = 4
    nnsolver = NeuralNetworkSolver(state_size, action_size)

    for e in range(episodes):
        state = initSTATE
        score = 0
        for time in range(times):
            movables = maze.get_movables(state)
            action = nnsolver.choose_action(state, movables)
            reward, done = maze.get_val(action)
            score = score + reward
            next_state = action
            next_movables = maze.get_movables(next_state)
            nnsolver.remember_memory(state, action, reward, next_state, next_movables, done)
            if done or time == (times - 1):
                if e % 10 == 0:
                    print(f"episode: {e}/{episodes}, score: {score}, e: {nnsolver.epsilon:.2} at {time}")

                break
            state = next_state
        # run experience replay after sampling the state, action and reward for defined times
        nnsolver.replay_experience(32)


if __name__ == "__main__":
    main()

