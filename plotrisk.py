import logging

import matplotlib.pyplot as plt
import numpy as np


def plot_risk(minr, maxr, cur, fname):
    ngrid = 100
    plt.subplots(figsize=(10, 3))
    x = np.linspace(minr, maxr, ngrid)
    y = np.zeros(ngrid)
    t = np.arange(ngrid)
    plt.scatter(x, y, marker='s', c=t, s=150, cmap='RdYlGn_r')
    plt.scatter([cur], [0], marker='o',  s=500, facecolors='none', edgecolors='k', linewidths=3)
    plt.text(maxr, -0.015, str(maxr), fontsize=18)
    plt.text(minr, -0.015, str(minr), fontsize=18)
    plt.text(cur, 0.0085, "{:.2f}".format(cur), fontsize=18)
    plt.axis('off')
    plt.savefig(fname, bbox_inches='tight')
    logging.info(f'plot and save riscmeter figure {fname}')
