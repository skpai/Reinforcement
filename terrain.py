import numpy as np
from matplotlib import pyplot as plt


class Terrain:
    def __init__(self, x_max=5, y_max=5, pts_nb=51, distrib="circle"):
        # initialize the variables
        self.x_max = x_max
        self.y_max = y_max
        self.pts_nb = pts_nb
        self.distrib = distrib
        self.x = np.linspace(-self.x_max, self.x_max, self.pts_nb)
        self.y = np.linspace(-self.y_max, self.y_max, self.pts_nb)

    def init_terrain_reward(self):
        xs, ys = np.meshgrid(self.x, self.y, sparse=True)
        if self.distrib == "circle":
            zs = np.sqrt(self.x_max**2 + self.y_max**2) - np.sqrt(xs**2 + ys**2)
        return zs

    def get_terrain_reward(self, x_ask, y_ask):
        # get reward value at given position x_ask and y_ask
        if self.distrib == "circle":
            rwd = np.sqrt(self.x_max**2 + self.y_max**2) - np.sqrt(
                x_ask**2 + y_ask**2
            )
        return rwd

    def plot_terrain(self, zs):

        h = plt.contourf(x, y, zs)
        plt.axis("scaled")
        plt.colorbar()
        plt.show()


def main():
    terrain = Terrain()
    print()
