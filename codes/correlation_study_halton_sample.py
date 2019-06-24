from max_tbr_finder_random import *
from scipy.stats import pearsonr
import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

def make_plot_correlation(filename, material):
    df=pd.read_json(filename)
    df_filtered = df.loc[(df['breeder_material_name']==material) & (df['graded']=='graded')]
    enrichment_first_layer = [item[0] for item in df_filtered['enrichment_value'].tolist()]
    enrichment_second_layer = [item[1] for item in df_filtered['enrichment_value'].tolist()]
    enrichment_third_layer = [item[2] for item in df_filtered['enrichment_value'].tolist()]
    enrichment_fourth_layer = [item[3] for item in df_filtered['enrichment_value'].tolist()]

    df_filtered.insert(4, 'enrichment_first_layer', enrichment_first_layer, True)
    df_filtered.insert(5, 'enrichment_second_layer', enrichment_second_layer, True)
    df_filtered.insert(6, 'enrichment_third_layer', enrichment_third_layer, True)
    df_filtered.insert(7, 'enrichment_fourth_layer', enrichment_fourth_layer, True)

    plt.rcParams['figure.figsize']=[100,40]
    fig, ax = plt.subplots(nrows=1, ncols=4)
    ax=ax.flatten()

    cols = ['enrichment_first_layer','enrichment_second_layer','enrichment_third_layer', 'enrichment_fourth_layer']
    colors =['#243AB5', '#243AB5', '#243AB5', '#243AB5']
    L = [enrichment_first_layer, enrichment_second_layer, enrichment_third_layer, enrichment_fourth_layer]
    tbr = list(df_filtered['value'])
    j=0

    for i in ax:
        if j==0:
            i.set_ylabel('TBR')
        i.scatter(L[j], tbr, alpha=0.5, color = colors[j])
        i.set_xlabel(cols[j])
        spearman = str(spearmanr(L[j],tbr)[0])
        pearson = str(pearsonr(L[j],tbr)[0])
        i.set_title('Pearson ' +str(material)+ ': \n' +pearson +'\n'+ 'Spearman ' +str(material)+ ': \n' +spearman)
        j+=1
    plt.show()
    return()

if __name__ == '__main__':
    make_plot_correlation('results/simulation_results_4_layers_halton_first_wall.json','Li')
