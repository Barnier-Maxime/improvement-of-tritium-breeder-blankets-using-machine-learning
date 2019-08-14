import pandas as pd
import sklearn
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from json_file_plot_results import *
from geometry_breeder_material import *
import random 
from inference.gp_tools import GpOptimiser

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

        bounds = [(0,1),(0,1)]
        GP = GpOptimiser(X, y, bounds=bounds)
        
        new_enrichment_value = list(GP.search_for_maximum())
        
        
        X.remove(row_min_tbr['enrichment_value'])
        y.remove(row_min_tbr['value'])

        print('new enrichment fraction', new_enrichment_value)
        append_to_json = find_tbr_dict(new_enrichment_value, material, True, 500000)
        #adjust the number of batches with the experiment
        X.append(new_enrichment_value)
        y.append(append_to_json['value'])

        with open('results_new_neutron_source/added_'+str(k)+'_result_2_layers_halton_first_wall_neural_network.json', 'w') as file_object:
            json.dump([append_to_json], file_object, indent=2)
                        
        print('file created')
        df_append = pd.read_json('results_new_neutron_source/added_'+str(k)+'_result_2_layers_halton_first_wall_neural_network.json')
        df_filtered = df_filtered.append(df_append, ignore_index=True, sort=True)

        idx = df_filtered.index[df_filtered['value']==row_min_tbr['value']]
        df_filtered = df_filtered.drop(idx[0])

    TBR = y
    print('The max TBR for '+str(len(X[0]))+' layers and '+str(material)+' is', max(TBR))
    


if __name__ == '__main__':
    #plot_prediction_color('results_new_neutron_source/simulation_results_2_layers_halton_first_wall_neural_network.json', 'Li')
    #plot_prediction_color('results_new_neutron_source/simulation_results_2_layers_halton_first_wall_neural_network.json', 'Li2TiO3')
    plot_prediction_color('results_new_neutron_source/simulation_results_2_layers_halton_first_wall_neural_network.json', 'Li4SiO4')

#The max TBR for 4 layers and Li is 0.9849869788697511
#The max TBR for 4 layers and Li2TiO3 is 0.985275764769823
#The max TBR for 4 layers and Li4SiO4 is 0.9930969825759731

#The max TBR for 2 layers and Li is 0.984885413145494
#The max TBR for 2 layers and Li2TiO3 is 0.985196941781273
#The max TBR for 2 layers and Li4SiO4 is 0.9938559087943191