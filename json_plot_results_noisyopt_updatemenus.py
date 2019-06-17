
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from mpl_toolkits.mplot3d import Axes3D
from pandas.io.json import json_normalize
from plotly.graph_objs import Layout, Scatter, Scatter3d
from plotly.offline import download_plotlyjs, plot

def make_plot(filename, material, include_first_wall):
    number_of_layers_plot=[]
    max_tbr_plot=[]
    trace =[]
    df =pd.read_json(filename) 
    filtered_df = df.loc[(df['breeder_material_name']==material) & (df['include_first_wall']==include_first_wall)]
    for number_of_layers in [1,2,3,4]:
        
        row_with_number_of_layers = df.loc[df['number_of_layers']==number_of_layers]
        #row_with_max_tbr_number_of_layers = df.loc[row_with_number_of_layers['max_tbr'].idxmax()]

        max_tbr = float(row_with_number_of_layers['max_tbr'])


        # PLOTS RESULTS #
        number_of_layers_plot.append(number_of_layers)
        max_tbr_plot.append(max_tbr)

    trace = Scatter(x=number_of_layers_plot, 
                    y=max_tbr_plot,
                    name='Optimized tbr',
                    mode = 'markers+lines',
                    )
    return(trace)


def make_buttons(titles):

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
    data=[]
    data.append(make_plot('results/result_noisyopt_Li_first_wall.json','Li',True))  #Li
    data.append(make_plot('results/result_noisyopt_Li_no_first_wall.json','Li',False)) 

    data.append(make_plot('results/result_noisyopt_Li4SiO4_first_wall.json','Li4SiO4',True)) #Li4SiO4
    data.append(make_plot('results/result_noisyopt_Li4SiO4_no_first_wall.json','Li4SiO4',False))

    data.append(make_plot('results/result_noisyopt_Li2TiO3_first_wall.json','Li2TiO3',True)) #Li2TiO3
    data.append(make_plot('results/result_noisyopt_Li2TiO3_no_first_wall.json','Li2TiO3',False))
    print(data)

    updatemenus = make_buttons(["Study with Li with first wall",
                                "Study with Li without first wall",

                                "Study with Li4SiO4 with first wall",
                                "Study with Li4SiO4 without first wall",

                                "Study with Li2TiO3 with first wall",
                                "Study with Li2TiO3 without first wall",
                                ])



    layout = go.Layout(title='Optimized max TBR with different materials with or without the first wall as a function of the number of layer',
                    scene=dict(
                                    xaxis=dict(
                                            title='Number of layer'
                                            ),
                                    yaxis=dict(
                                            title='Max TBR'
                                    )
                                ),
                        updatemenus = updatemenus
                        )
    fig = go.Figure(data=data, layout=layout)
    plot(fig,show_link=True,filename = 'plots/simulation_results_noisy_opt_different_materials.html',image='png')
