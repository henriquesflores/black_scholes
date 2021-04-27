import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_table(table: pd.DataFrame) -> plt.Axes:
    plt.figure(figsize = (20, 10))

    color = sns.color_palette("RdBu", as_cmap = True)
    axis = sns.heatmap( table                          \
                      , annot = True                   \
                      , cmap = color                   \
                      , cbar = False                   \
                      , linewidths = 0.5               \
                      , robust = True                  \
                      , fmt = ",.0f"                   \
                      , annot_kws ={'size': 12}        \
    )

    return axis

def save_table_heatmap(heatmap: plt.Axes, where: os.path) -> None:
    heatmap.get_figure().savefig(where)
    return 
