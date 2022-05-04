import numpy as np
from matplotlib import pyplot as plt

class Maze:
    def __init__(self, rows=5, cols=5, target_positions=None, start_pos=None):
    # initialize the variables
        self.rows = rows
        self.cols = cols
        self.target_positions = target_positions
        self.start_pos = start_pos
        self.reward_matrix = -1+np.zeros((rows, cols))
        if target_positions:
            for position in target_positions:
                self.reward_matrix[position] = 100
    
    def check_start_pos(self):
        return self.start_pos not in self.target_positions  

    def plot_maze(self):
        plt.imshow(self.reward_matrix)
        plt.grid()
        plt.show()

    

def main():
    maze = Maze(rows=5, cols=5, target_positions=[(0,0), (4,3)])
    maze.plot_maze()
    

if __name__ == '__main__':
    main()





            


