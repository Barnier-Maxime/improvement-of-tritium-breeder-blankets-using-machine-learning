import openmc
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from material_maker_functions import *
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter3d, Layout, Scatter
import pandas as pd
from pandas.io.json import json_normalize

#################### ONLY WORKS FOR 3 LAYERS ########################
with open('simulation_results_'+str(3)+'_layers_non_uni_20000.json') as f:
    results_1 = json.load(f)

with open('simulation_results_'+str(3)+'_layers_uni_.json') as f:
    results_2 = json.load(f)
# PLOTS RESULTS #
x_axis_1 = []
y_axis_1 = []
z_axis_1 = []
x_axis_2 = []
y_axis_2 = []
z_axis_2 = []
TBR_1 = []
TBR_2 = []
text_list_1 =[]
text_list_2 = []
#print(results)
for k in results_1: # creation of the 3 axis
    x_axis_1.append(k['enrichment_value'][0])
    y_axis_1.append(k['enrichment_value'][1])
    z_axis_1.append(k['enrichment_value'][2])
    TBR_1.append(k['value'])
    text_list_1.append('TBR=' +str(k['value'])+'<br>'
                    +'Enrichment first layer=' +str(k['enrichment_value'][0])+'<br>'
                    +'Enrichment second layer=' +str(k['enrichment_value'][1])+'<br>'
                    +'Enrichment third layer=' +str(k['enrichment_value'][2])
                    )

results_df_1 = json_normalize(data=results_1)

for k in results_2: # creation of the 3 axis
    x_axis_2.append(k['enrichment_value'][0])
    y_axis_2.append(k['enrichment_value'][1])
    z_axis_2.append(k['enrichment_value'][2])
    TBR_2.append(k['value'])
    text_list_2.append('TBR=' +str(k['value'])+'<br>'
                    +'Enrichment first layer=' +str(k['enrichment_value'][0])+'<br>'
                    +'Enrichment second layer=' +str(k['enrichment_value'][1])+'<br>'
                    +'Enrichment third layer=' +str(k['enrichment_value'][2])
                    )

results_df_2 = json_normalize(data=results_2)

trace1 = go.Scatter3d(
    x=x_axis_1,
    y=y_axis_1,
    z=z_axis_1,
    hoverinfo='text',
    text=text_list_1,
    mode='markers',
    marker=dict(
        size=2,
        color=TBR_1,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)

trace2 = go.Scatter3d(
    x=x_axis_2,
    y=y_axis_2,
    z=z_axis_2,
    hoverinfo='text',
    text=text_list_2,
    mode='markers',
    marker=dict(
        size=2,
        color=TBR_2,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)

trace3 = go.Scatter3d(
    x=x_axis_1 + x_axis_2,
    y=y_axis_1 + y_axis_2,
    z=z_axis_1 + z_axis_2,
    hoverinfo='text',
    text=text_list_1 + text_list_2,
    mode='markers',
    marker=dict(
        size=2,
        color=TBR_1 + TBR_2,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)

data = [trace1, trace2, trace3]

updatemenus = list([
    dict(active=-1,
         buttons=list([   
            dict(label = 'Non uniform enrichment',
                 method = 'update',
                 args = [{'visible': [True, False, False]},
                         {'title': 'TBR with non uniform enrichment fraction'
                          }]),
            dict(label = 'Uniform enrichment',
                 method = 'update',
                 args = [{'visible': [False, True, False]},
                         {'title': 'TBR with uniform enrichment fraction'
                          }]),
            dict(label = 'Both',
                 method = 'update',
                 args = [{'visible': [False, False, True]},
                         {'title': 'Both type of enrichment'
                          }])
        ]),
    )
])

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
plot(fig,show_link=True,image='png')
