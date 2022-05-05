import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from maze import *
import random
from time import * 
from visualizer import *



class Agent:
    def __init__(self, maze, epsilon, gamma, alpha, 
                 state, q_table, actions=['up', 'down', 'left', 'right']):
        self.maze=maze
        self.epsilon = epsilon 
        self.gamma = gamma  
        self.alpha = alpha
        self.state = state 
        self.actions = actions
        self.q_table = q_table 
    
    def choose_action(self):
        state_actions = self.q_table[self.state]
        randomRate = np.random.uniform()
        if randomRate > self.epsilon:
            return self.actions.index(np.random.choice(self.actions)) 

        else:
            return state_actions.argmax()
    
    def update_q_table(self, reward, action, nxt_state):
        q_predict = self.q_table[self.state][action]
        if nxt_state in ['win', 'ghost'] :
            q_target = reward
        else:
            q_target = reward + self.gamma * self.q_table[nxt_state][action]
        self.q_table[self.state][action] += self.alpha * (q_target - q_predict) 
        self.state = nxt_state



def path(state, is_terminated):
    print(state, end='')
    if not is_terminated: print(' > ', end='')

def play():
    EPISODES = 20
    ACTIONS = ['up', 'down', 'left', 'right']
    initSTATE = (0,0)
    SIZE = (5,5) # maze size

    EPSILON = 0.9
    GAMMA = 0.9
    ALPHA = 0.1
    target = [(3,1), (4,4)]
    t_reward = 100
    f_reward_list = -1+np.zeros(SIZE)
    maze = Maze(ACTIONS)
    maze.build_map(SIZE, target, t_reward)
    Q_table = maze.create_q_table()
    agent = Agent(maze,epsilon= EPSILON, gamma= GAMMA, alpha= ALPHA,
             state = initSTATE, actions= ACTIONS,q_table= Q_table.copy())
    
    fig, ax= plt.subplots()


# main process RL - Q_Learning
    for episode in range(EPISODES):
        agent.state = initSTATE
        is_terminated = False
        count = 0
        while not is_terminated :
            action = agent.choose_action()
            nxt_state, reward = maze.env_feedback(state=agent.state, action=action)
            if agent.state == nxt_state: 
                reward = -10
            agent.update_q_table(reward=reward, action=action, nxt_state=nxt_state)
            
            if nxt_state in ['win']:
                is_terminated = True
            path(agent.state, is_terminated)
            try:
                animate(agent.state, maze.map, ax)
            except:
                pass
            agent.state = nxt_state
            count +=1
            return nxt_state
            
        print('\n Episode. '+str(episode)+' finished ... ,total step : '+str(count))
        time.sleep(2)

def main():
    EPISODES = 20
    ACTIONS = ['up', 'down', 'left', 'right']
    initSTATE = (0,0)
    SIZE = (5,5) # maze size

    EPSILON = 0.9
    GAMMA = 0.9
    ALPHA = 0.1
    target = [(3,1), (4,4)]
    t_reward = 100
    f_reward_list = -1+np.zeros(SIZE)
    maze = Maze(ACTIONS)
    maze.build_map(SIZE, target, t_reward)
    Q_table = maze.create_q_table()
    agent = Agent(maze,epsilon= EPSILON, gamma= GAMMA, alpha= ALPHA,
             state = initSTATE, actions= ACTIONS,q_table= Q_table.copy())


# main process RL - Q_Learning
    fig, ax= plt.subplots()
    for episode in range(EPISODES):
        agent.state = initSTATE
        is_terminated = False
        count = 0
        while not is_terminated :
            action = agent.choose_action()
            nxt_state, reward = maze.env_feedback(state=agent.state, action=action)
            if agent.state == nxt_state: 
                reward = -10
            ###########################################
            agent.update_q_table(reward=reward, action=action, nxt_state=nxt_state)
            
            if nxt_state in ['win']:
                is_terminated = True
                nxt_state = (0,0)

            path(agent.state, is_terminated)
            try:
                animate(agent.state, maze.map, ax)
            except:
                pass
            agent.state = nxt_state
            count +=1
            #time.sleep(0.05)
            
        print('\n Episode. '+str(episode)+' finished ... ,total step : '+str(count))
        #time.sleep(2)


if __name__ == "__main__":
    main()
