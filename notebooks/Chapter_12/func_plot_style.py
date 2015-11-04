import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import numpy as np

sns.set(context='talk')
sns.set_style("ticks", {"xtick.major.size": 4, "ytick.major.size": 4})

rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def subplots(**kwargs):
    "Custom subplots with axes throught the origin"
    #with sns.color_palette("Set2", 10):
    with sns.color_palette("muted"):
        if kwargs:
            fig, ax = plt.subplots(**kwargs)
        else:
            fig, ax = plt.subplots()

        def reset_spine(ax):
            # Set the axes through the origin
            for spine in ['left', 'bottom']:
                ax.spines[spine].set_position('zero')
            for spine in ['right', 'top']:
                ax.spines[spine].set_color('none')

            # Only show ticks on the left and bottom spines
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')

            return ax

        if isinstance(ax, np.ndarray):
            tmp = [reset_spine(a) for a in ax]
            ax = tmp
        else:
            ax = reset_spine(ax)

        return plt, fig, ax



