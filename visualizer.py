import numpy as np
from matplotlib import pyplot as plt
from prospect import *


class Visualizer:
    def __init__(self, x, y, reward):
        # self.steps = steps
        self.x = x
        self.y = y
        self.reward = reward

    def plot_terrain(self):
        x, y=self.x, self.y
        reward=self.reward

        plt.scatter(x, y, s=reward)
        plt.set_xlabel("x")
        plt.set_ylabel("y")
        plt.show()

    def plot_cumulative_rwd(self):
        cdf = np.cumsum(self.reward)
        plt.plot(self.steps, cdf)

    def plot_dashboard(self):

        with plt.style.context(("seaborn", "ggplot")):
            fig = plt.figure(constrained_layout=True, figsize=(10, 8))
            specs = gridspec.GridSpec(
                ncols=2, nrows=1, figure=fig
            )  ## Declaring 2x2 figure.

            ax1 = fig.add_subplot(specs[0, 0])  ## First Row
            ax2 = fig.add_subplot(specs[0, 1])  ## Second Row First Column

            ## First Graph -  Scatter Plot
            ax1.plot_terrain(self)
            ax1.set_title("x=%s, y=%s" % (self.x_i, self.y_i))
            ax1.legend(title="Reward value", loc="best")

            ## Second Graph - Cumulative Chart
            ax2.plot_cumulative_rwd(self)
            ax2.set_ylabel(plot2_f)
            ax2.set_title(
                "Cumulative reward so far, for step number%s" % self.steps[-1]
            )

            plt.close(fig)
            return fig

def main():
    pass



if __name__ == "__main__":
    main()
