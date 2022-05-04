import numpy as np
from matplotlib import pyplot as plt

class Maze:
    def __init__(self, rows=5, cols=5, pts_nb=51, distrib="circle"):
    # initialize the variables
    self.x_max = x_max
    self.y_max = y_max
    self.pts_nb = pts_nb
    self.distrib = distrib
    self.x = np.linspace(-self.x_max, self.x_max, self.pts_nb)
    self.y = np.linspace(-self.y_max, self.y_max, self.pts_nb)