
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

def make_trace_from_json(filename,material,graded,include_first_wall):

    #################### ONLY WORKS FOR 3 LAYERS ########################
    df =pd.read_json(filename) 
    filtered_df = df.loc[(df['breeder_material_name']==material) & (df['graded']==graded) & (df['first_wall']==include_first_wall)]

    # PLOTS RESULTS #
    x_axis = [item[0] for item in filtered_df['enrichment_value'].tolist()]
    y_axis = [item[1] for item in filtered_df['enrichment_value'].tolist()]
    z_axis = [item[2] for item in filtered_df['enrichment_value'].tolist()]
    TBR = filtered_df['value'].tolist()
    std_dev = filtered_df['std_dev'].tolist()

    text_list =[]

    for x,y,z,t,s in zip(x_axis,y_axis,z_axis,TBR,std_dev):
        text_list.append('TBR=' +str(round(t,5))+' +- '+str(round(s,5))+'<br>'
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
    return trace

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



data=[]
data.append(make_trace_from_json('results/simulation_results_layers_random.json','Li','graded',True))
data.append(make_trace_from_json('results/simulation_results_layers_random_no_first-wall.json','Li','graded',True)) #True that there is no 

data.append(make_trace_from_json('results/simulation_results_layers_random.json','Li','uniform',True))
data.append(make_trace_from_json('results/simulation_results_layers_random_no_first-wall.json','Li','uniform',True))

data.append(make_trace_from_json('results/simulation_results_layers_random.json','Li4SiO4', 'graded',True))
data.append(make_trace_from_json('results/simulation_results_layers_random_no_first-wall.json','Li4SiO4', 'graded',True))

data.append(make_trace_from_json('results/simulation_results_layers_random.json','Li4SiO4', 'uniform',True))
data.append(make_trace_from_json('results/simulation_results_layers_random_no_first-wall.json','Li4SiO4', 'uniform',True))

data.append(make_trace_from_json('results/simulation_results_layers_random.json','Li2TiO3', 'graded',True))
data.append(make_trace_from_json('results/simulation_results_layers_random_no_first-wall.json','Li2TiO3', 'graded',True))

data.append(make_trace_from_json('results/simulation_results_layers_random.json','Li2TiO3', 'uniform',True))
data.append(make_trace_from_json('results/simulation_results_layers_random_no_first-wall.json','Li2TiO3', 'uniform',True))


updatemenus = make_buttons(["TBR with non uniform enrichment fraction and Li with first wall",
                            "TBR with non uniform enrichment fraction and Li without first wall",

                            "TBR with uniform enrichment fraction and Li with first wall",
                            "TBR with uniform enrichment fraction and Li without first wall",

                            "TBR with non uniform enrichment fraction and Li4SiO4 with first wall",
                            "TBR with non uniform enrichment fraction and Li4SiO4 without first wall",

                            "TBR with uniform enrichment fraction and Li4SiO4 with first wall",
                            "TBR with uniform enrichment fraction and Li4SiO4 without first wall",

                            "TBR with non uniform enrichment fraction and Li2TiO3 with first wall",
                            "TBR with non uniform enrichment fraction and Li2TiO3 without first wall",

                            "TBR with uniform enrichment fraction and Li2TiO3 with first wall",
                            "TBR with uniform enrichment fraction and Li2TiO3 without first wall" ])



layout = go.Layout(title='TBR as a function of enrichment fractions in Li6',
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
plot(fig,show_link=True,filename = 'plots/simulation_results_layers_random_no_first_wall.html',image='png')
