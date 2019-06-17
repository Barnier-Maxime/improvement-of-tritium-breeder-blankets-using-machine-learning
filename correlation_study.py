from scipy.stats import pearsonr
import pandas as pd

def correlation_layers_tbr(filename):
    df = pd.read_json(filename)
    nbr_of_layers = list(df['number_of_layers'])
    max_tbr = list(df['max_tbr'])
    
    corr = pearsonr(nbr_of_layers,max_tbr)
    return(corr)

def correlation_enrichment_tbr(filename, layer_to_consider): #we cannot calculate a correlation between the enrichment fractions and the tbr but only between the enrichment fraction of a particular layer and the tbr
    df = pd.read_json(filename)
    df_filtered = df.loc[df['number_of_layers']>layer_to_consider-1]
    enrichment_layer = [item[layer_to_consider-1] for item in df_filtered['best_enrichment'].tolist()]
    
    max_tbr = list(df_filtered['max_tbr'])

    if len(set(enrichment_layer))!=1 and len(set(max_tbr))!=1:
        corr = pearsonr(enrichment_layer, max_tbr)
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
