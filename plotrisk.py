import matplotlib.pyplot as plt
import numpy as np


def plot_risk(minr, maxr, cur):
    ngrid = 100
    plt.subplots()
    x = np.linspace(minr, maxr, ngrid)
    y = np.zeros(ngrid)
    t = np.arange(ngrid)
    print(int(cur * ngrid / (maxr - minr)))
    plt.scatter(x, y, marker='s', c=t, s=100, cmap='RdYlGn_r')
    plt.scatter([cur], [0], marker='o',  s=500, facecolors='none', edgecolors='k', linewidths=3)
    plt.text(maxr, -0.01, str(maxr), fontsize=18)
    plt.text(minr, -0.01, str(minr), fontsize=18)
    plt.text(cur, 0.007, str(cur), fontsize=18)
    plt.axis('off')
    plt.show()
