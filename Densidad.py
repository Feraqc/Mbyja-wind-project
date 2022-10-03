import matplotlib.pyplot as plt
import random as rm

def repr_den(density):
    x = []
    y = []
    fig, ax = plt.subplots()
    for j in range(int(density*1000)):
        x.append(rm.uniform(0, 10000))
        y.append(rm.uniform(0, 10000))
    ax.scatter(x, y)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return fig