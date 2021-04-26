import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

from black_scholes_functions import *
from utils.data_handling import *


def scenario_table(table_name):

    
    sns.set()
    plt.figure(figsize=(20, 10))
    ax = sns.heatmap(table_name, annot=True,cmap ="RdBu", linewidths = 0.5,cbar=False, robust=True, fmt=".0f",annot_kws={'size':12}, center=0)
    for t in ax.texts: t.set_text('${:,.0f}'.format(float(t.get_text())))
    plt.show()
    tab= table_name.name +'.png'
    ax.get_figure().savefig(tab) 
    return 