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

        bounds = [(0,1),(0,1),(0,1)]
        GP = GpOptimiser(X,y,bounds=bounds)
        
        X.remove(row_min_tbr['enrichment_value'])
        y.remove(row_min_tbr['value'])

        print(GP.search_for_maximum()[0])
        input()
        #print('new enrichment fraction', new_enrichment_value)
        
        append_to_json = find_tbr_dict(new_enrichment_value, material, True, 500000)
        #adjust the number of batches with the experiment
        X.append(new_enrichment_value)
        y.append(append_to_json['value'])

        with open('results_new_neutron_source/added_'+str(k)+'_result_3_layers_halton_first_wall_neural_network.json', 'w') as file_object:
            json.dump([append_to_json], file_object, indent=2)
                        
        print('file created')
        df_append = pd.read_json('results_new_neutron_source/added_'+str(k)+'_result_3_layers_halton_first_wall_neural_network.json')
        df_filtered = df_filtered.append(df_append, ignore_index=True, sort=True)

        idx = df_filtered.index[df_filtered['value']==row_min_tbr['value']]
        df_filtered = df_filtered.drop(idx[0])


    x_axis = [item[0] for item in X]
    y_axis = [item[1] for item in X]
    z_axis = [item[2] for item in X]

    TBR = y
    text_list =[]

    for x,y,z,t in zip(x_axis,y_axis,z_axis,TBR):
        text_list.append('TBR=' +str(round(t,5)) + '<br>'
                        +'Enrichment first layer=' +str(round(x,5))+'<br>'
                        +'Enrichment second layer=' +str(round(y,5))+'<br>'
                        +'Enrichment third layer=' +str(round(z,5))
                        )

    trace = go.Scatter3d(
        x=x_axis,
        y=y_axis,
        z=z_axis,
        hoverinfo='text',
        text=text_list,
        mode='markers',
        marker=dict(
            size=2,
            color=TBR,                # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            colorbar=dict(title='TBR'),
            opacity=0.8
        )
    )
    return(trace)

def make_buttons_bis(titles):
    
    button_discriptions = []
    
    for i, title in enumerate(titles):
        true_false_list=[False]*len(titles)
        true_false_list[i] = True
        button_discriptions.append(dict(label = title,
                                   method = 'update',
                                   args = [{'visible': true_false_list},
                                   {'title': title
                                   }]))

    updatemenus = list([
        dict(active=-1,
            buttons=list(button_discriptions),
        )
    ])

    return updatemenus

if __name__ == '__main__':
    data = []
    data.append(plot_prediction_color('results_new_neutron_source/simulation_results_3_layers_halton_first_wall_neural_network.json', 'Li'))
    data.append(plot_prediction_color('results_new_neutron_source/simulation_results_3_layers_halton_first_wall_neural_network.json', 'Li2TiO3'))
    data.append(plot_prediction_color('results_new_neutron_source/simulation_results_3_layers_halton_first_wall_neural_network.json', 'Li4SiO4'))

    updatemenus = make_buttons_bis(['TBR prediction 3 layers for Li',
                                'TBR prediction 3 layers for Li2TiO3',
                                'TBR prediction 3 layers for Li4SiO4'])

    layout = go.Layout(title='TBR prediction as a function of enrichment fractions in Li6',
                    scene=dict(
                                    xaxis=dict(
                                            title='Enrichment first layer'
                                            ),
                                    yaxis=dict(
                                            title='Enrichment second layer'
                                    ),
                                    zaxis=dict(
                                            title='Enrichment third layer'
                                    )
                                ),
                        updatemenus = updatemenus
                        )
    
    fig = go.Figure(data=data, layout=layout)
    plot(fig,show_link=True,filename = 'plots_new_neutron_source/prediction_results_3_layers_inference.html',image='png')