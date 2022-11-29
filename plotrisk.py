import matplotlib.pyplot as plt
import numpy as np


def plot_risk(min, max, cur):
    ngrid = 100
    plt.subplots()
    x = np.linspace(min, max, ngrid)
    y = np.zeros(ngrid)
    t = np.arange(ngrid)
    print(int(cur*ngrid/(max-min)))
    plt.scatter(x, y, marker='s', c=t, s=100, cmap='RdYlGn_r')
    plt.scatter([cur], [0], marker='o',  s=500, facecolors='none', edgecolors='k', linewidths=3)
    plt.text(max, -0.01, str(max), fontsize=18)
    plt.text(min, -0.01, str(min), fontsize=18)
    plt.text(cur, 0.007, str(cur), fontsize=18)
    plt.axis('off')
    plt.show()
