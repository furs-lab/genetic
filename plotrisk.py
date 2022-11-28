import matplotlib.pyplot as plt
import numpy as np


def plotrisk(min, max, cur):
    ngrid = 100
    curn = (cur - min)*ngrid/max
    plt.subplots()
    gradient = np.linspace(0, 1, ngrid)
    gradient = np.vstack((gradient, gradient))
    plt.imshow(gradient, aspect=2, cmap='rainbow')
    plt.text(ngrid - ngrid / 10, 4, str(max), fontsize=18)
    plt.text(0, 4, str(min), fontsize=18)
    plt.text(curn-5, -2, str(cur), fontsize=18)
    plt.scatter([curn], [0.5], marker='o', c='navy', s=300)
    # plt.scatter([curn], [2], marker='^', c='k', s=200)
    # plt.scatter([curn], [-1], marker='v', c='k', s=200)
    plt.axis('off')
    plt.show()
