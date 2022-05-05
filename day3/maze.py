import numpy as np
from matplotlib import pyplot as plt

class Maze:
    def __init__(self, actions):
        self.actions = actions
        
    def build_map(self, size, target, t_reward):
        self.size = size
        self.target = target
        self.map = -1+np.zeros((size))
        self.all_positions=[(i,j) for i in range(size[0]) for j in range(size[1])]
        for item in target:
            x,y=item
            self.map[x,y] = t_reward
        return
    
    def env_feedback(self, state, action):
        nxt_state = self.cal_coordinate(state, action)
        
        reward = self.map[nxt_state]
        if nxt_state in self.target:
            nxt_state = 'win'
            
        return nxt_state, reward
    
    def cal_coordinate(self, state, action):
        next_state = ()
        if action == 0:
            next_state = (state[0] - 1, state[1])
        elif action == 1:
            next_state = (state[0] + 1, state[1])
        elif action == 2:
            next_state = (state[0], state[1] + 1)
        elif action == 3:
            next_state = (state[0], state[1] - 1)
        if next_state not in self.all_positions:
            next_state=state
        return next_state
    
    def plot_maze_new(self):
        plt.pcolor(self.map, edgecolors='w', linewidths=2)
        plt.show()
    
    def create_q_table(self):
        q_table = np.zeros(self.size + (len(self.actions),))
        print('Q_table.shape :')
        print(q_table.shape)
        return np.array(q_table)
        

def main():
    maze = Maze(rows=5, cols=5, target_positions=[(0,0), (4,3)])
    maze.plot_maze_new()
    

if __name__ == '__main__':
    main()





            


