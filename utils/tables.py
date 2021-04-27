import matplotlib.pyplot as plt
import seaborn as sns 


def scenario_table(table_name):

    
    
    plt.figure(figsize=(20, 10))
    color=sns.color_palette("Blues_r", as_cmap=True)
    ax = sns.heatmap(table_name, annot=True,cmap=color,cbar=False, linewidths = 0.5, robust=True, fmt=".0f",annot_kws={'size':12}, center=0)
    #ax = sns.heatmap(table_name, annot=True,cmap ="RdBu", linewidths = 0.5,cbar=False, robust=True, fmt=".0f",annot_kws={'size':12}, center=0)
    for t in ax.texts: t.set_text('${:,.0f}'.format(float(t.get_text())))
    
    tab= directory +"\\"+table_name.name +'.png'
    ax.get_figure().savefig(tab) 
    return 