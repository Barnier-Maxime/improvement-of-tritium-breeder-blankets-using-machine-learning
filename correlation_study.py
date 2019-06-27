from scipy.stats import pearsonr
import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

def correlation_layers_tbr(filename):
    df = pd.read_json(filename)
    nbr_of_layers = list(df['number_of_layers'])
    max_tbr = list(df['max_tbr'])
    
    corr = spearmanr(nbr_of_layers,max_tbr)
    return(corr)

def correlation_enrichment_tbr(filename, layer_to_consider): #we cannot calculate a correlation between the enrichment fractions and the tbr but only between the enrichment fraction of a particular layer and the tbr
    df = pd.read_json(filename)
    df_filtered = df.loc[df['number_of_layers']>layer_to_consider-1]
    enrichment_layer = [item[layer_to_consider-1] for item in df_filtered['best_enrichment'].tolist()]
    
    max_tbr = list(df_filtered['max_tbr'])

    if len(set(enrichment_layer))!=1 and len(set(max_tbr))!=1:
        corr = spearmanr(enrichment_layer, max_tbr)
        return(corr)
    else:
        return('impossible correlation because same numbers for the enrichment values')

################# Correlation between tbr and number of layers ###################

print('Pearson coeff layers Li with first wall = ', correlation_layers_tbr('results/result_noisyopt_Li_first_wall.json'))
print('Pearson coeff layers Li without first wall = ', correlation_layers_tbr('results/result_noisyopt_Li_no_first_wall.json'))

print('Pearson coeff layers Li4SiO4 with first wall = ', correlation_layers_tbr('results/result_noisyopt_Li4SiO4_first_wall.json'))
print('Pearson coeff layers Li4SiO4 without first wall = ', correlation_layers_tbr('results/result_noisyopt_Li4SiO4_no_first_wall.json'))

print('Pearson coeff layers Li2TiO3 with first wall = ', correlation_layers_tbr('results/result_noisyopt_Li2TiO3_first_wall.json'))
print('Pearson coeff layers Li2TiO3 without first wall = ', correlation_layers_tbr('results/result_noisyopt_Li2TiO3_no_first_wall.json'))

################ Correlation between tbr and layer to consider #########################

for k in range(3):
    print('Pearson coeff layer ' +str(k+1)+ ' Li with first wall = ', correlation_enrichment_tbr('results/result_noisyopt_Li_first_wall.json', int(k+1)))
    print('Pearson coeff layer ' +str(k+1)+ ' Li without first wall = ', correlation_enrichment_tbr('results/result_noisyopt_Li_no_first_wall.json', int(k+1)))

    print('Pearson coeff layer ' +str(k+1)+ ' Li4SiO4 with first wall = ', correlation_enrichment_tbr('results/result_noisyopt_Li4SiO4_first_wall.json', int(k+1)))
    print('Pearson coeff layer ' +str(k+1)+ ' Li4SiO4 without first wall = ', correlation_enrichment_tbr('results/result_noisyopt_Li4SiO4_no_first_wall.json', int(k+1)))

    print('Pearson coeff layer ' +str(k+1)+ ' Li2TiO3 with first wall = ', correlation_enrichment_tbr('results/result_noisyopt_Li2TiO3_first_wall.json', int(k+1)))
    print('Pearson coeff layer ' +str(k+1)+ ' Li2TiO3 without first wall = ', correlation_enrichment_tbr('results/result_noisyopt_Li2TiO3_no_first_wall.json', int(k+1)))

def make_plot_correlation(filename):
    df = pd.read_json(filename)
    plt.rcParams['figure.figsize']=[100,40]
    fig, ax = plt.subplots(nrows=1, ncols=4)
    ax=ax.flatten()

    cols = ['number_of_layers','enrichment_first_layer','enrichment_second_layer','enrichment_third_layer']
    colors =['#415952', '#f35134', '#243AB5', '#243AB5']
    number_of_layers = list(df['number_of_layers'])

    df_filtered_1 = df.loc[df['number_of_layers']>0]
    enrichment_first_layer = [item[0] for item in df_filtered_1['best_enrichment'].tolist()]
    max_tbr_1 = list(df_filtered_1['max_tbr'])

    df_filtered_2 = df.loc[df['number_of_layers']>1]
    enrichment_second_layer = [item[1] for item in df_filtered_2['best_enrichment'].tolist()]
    max_tbr_2 = list(df_filtered_2['max_tbr'])

    df_filtered_3 = df.loc[df['number_of_layers']>2]
    enrichment_third_layer = [item[2] for item in df_filtered_3['best_enrichment'].tolist()]
    max_tbr_3 = list(df_filtered_3['max_tbr'])

    L = [number_of_layers, enrichment_first_layer, enrichment_second_layer, enrichment_third_layer]
    M = [max_tbr_1, max_tbr_1, max_tbr_2, max_tbr_3]
    N = [df_filtered_1, df_filtered_1, df_filtered_2, df_filtered_3]
    j=0

    for i in ax:
        if j==0:
            i.set_ylabel('TBR')
        i.scatter(L[j], M[j], alpha=0.5, color = colors[j])
        i.set_xlabel(cols[j])
        spearman = str(spearmanr(L[j],M[j])[0])
        pearson = str(pearsonr(L[j],M[j])[0])
        i.set_title('Pearson : \n' +pearson +'\n'+ 'Spearman : \n' +spearman)
        j+=1
    plt.show()
    return()

if __name__ == '__main__':
    make_plot_correlation('results/result_noisyopt_Li_no_first_wall.json')

