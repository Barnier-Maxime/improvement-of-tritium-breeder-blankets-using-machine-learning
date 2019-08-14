import pandas as pd
import sklearn
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from json_file_plot_results import *
from geometry_breeder_material import *
import random 
import ghalton

def plot_prediction_color(filename, material):
    df = pd.read_json(filename)
    df_filtered = df.loc[df['breeder_material_name']==material]

    for k in range(1,100):  #improvement of the dataset we remove the worst tbr values and we had a better enrichment configuration to replace it
        X = list(df_filtered['enrichment_value'])
        y = list(df_filtered['value'])
        kernel = DotProduct() + WhiteKernel()
        gpr = GaussianProcessRegressor(kernel = kernel, random_state=0).fit(X,y)
        gpr.score(X,y)
        row_max_tbr = df_filtered.loc[df_filtered['value'].idxmax()]
        row_min_tbr = df_filtered.loc[df_filtered['value'].idxmin()]

        X.remove(row_min_tbr['enrichment_value'])
        y.remove(row_min_tbr['value'])
        
        new_enrichment_value = []
        new_enrichment_value.append(row_max_tbr['enrichment_value'][0] + random.uniform(0, 1-row_max_tbr['enrichment_value'][0]))
        new_enrichment_value.append(row_max_tbr['enrichment_value'][1] + random.uniform(0, 1-row_max_tbr['enrichment_value'][1]))
        new_enrichment_value.append(row_max_tbr['enrichment_value'][2] + random.uniform(0, 1-row_max_tbr['enrichment_value'][2]))
        new_enrichment_value.append(row_max_tbr['enrichment_value'][3] + random.uniform(0, 1-row_max_tbr['enrichment_value'][3]))

        print('new enrichment fraction', new_enrichment_value)
        append_to_json = find_tbr_dict(new_enrichment_value, material, True, 1000000)
        #adjust the number of batches with the experiment
        X.append(new_enrichment_value)
        y.append(append_to_json['value'])

        with open('results_new_neutron_source/added_'+str(k)+'_result_4_layers_halton_first_wall_neural_network.json', 'w') as file_object:
            json.dump([append_to_json], file_object, indent=2)
                            
        print('file created')
        df_append = pd.read_json('results_new_neutron_source/added_'+str(k)+'_result_4_layers_halton_first_wall_neural_network.json')
        df_filtered = df_filtered.append(df_append, ignore_index=True, sort=True)

        idx = df_filtered.index[df_filtered['value']==row_min_tbr['value']]
        df_filtered = df_filtered.drop(idx[0])
    
    y_predicted = gpr.predict(X)
    TBR = y_predicted
    print('The max TBR with the gaussian process for ' + str(len(X[0])) + ' layers is of', max(TBR))

if __name__ == '__main__':
    #plot_prediction_color('results_new_neutron_source/simulation_results_4_layers_halton_first_wall_neural_network.json', 'Li')
    #plot_prediction_color('results_new_neutron_source/simulation_results_4_layers_halton_first_wall_neural_network.json', 'Li2TiO3')
    plot_prediction_color('results_new_neutron_source/simulation_results_4_layers_halton_first_wall_neural_network.json', 'Li4SiO4')

#The max TBR with the gaussian process for 2 layers and lithium is of 0.9826561263325857
#The max TBR with the gaussian process for 2 layers and Li2TiO3 is of 0.9838664158828578
#The max TBR with the gaussian process for 2 layers and Li4SiO4 is of 0.991781569417725

#The max TBR with the gaussian process for 4 layers and lithium is of 0.9840929309664261
#The max TBR with the gaussian process for 4 layers and Li2TiO3 is of 0.9848257307421733
#The max TBR with the gaussian process for 4 layers and Li4SiO4 is of 0.9925454544290915

