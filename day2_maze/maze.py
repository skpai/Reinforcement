import numpy as np
from matplotlib import pyplot as plt

class Maze:
    def __init__(self, rows=5, cols=5, target_positions=None, start_pos=None, ghost_positions=None):
    # initialize the variables
        self.rows = rows
        self.cols = cols
        self.target_positions = target_positions
        self.start_pos = start_pos
        self.reward_matrix = -1+np.zeros((rows, cols))
        self.ghost_positions = ghost_positions
        if target_positions:
            for position in target_positions:
                self.reward_matrix[position] = 100
        
    
    def check_start_pos(self):
        return self.start_pos not in self.target_positions
    def get_all_points(self):
        return [(i,j) for i in range(self.rows) for j in range(self.cols)]  

    def plot_maze(self):
        plt.imshow(self.reward_matrix)
        plt.grid()
        plt.show()

    def plot_maze_new(self):
        plt.pcolor(self.reward_matrix, edgecolors='w', linewidths=2)
        plt.show()

# class Tile:
#     def __init__(self, type="empty"):
        

def main():
    maze = Maze(rows=5, cols=5, target_positions=[(0,0), (4,3)])
    maze.plot_maze_new()
    

if __name__ == '__main__':
    main()





            


