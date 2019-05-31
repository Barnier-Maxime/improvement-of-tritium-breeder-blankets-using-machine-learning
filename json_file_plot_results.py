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
    results = json.load(f)

# PLOTS RESULTS #
x_axis = []
y_axis = []
z_axis = []
TBR = []
text_list =[]
#print(results)
for k in results: # creation of the 3 axis
    x_axis.append(k['enrichment_value'][0])
    y_axis.append(k['enrichment_value'][1])
    z_axis.append(k['enrichment_value'][2])
    TBR.append(k['value'])
    text_list.append('TBR=' +str(k['value'])+'<br>'
                    +'Enrichment first layer=' +str(k['enrichment_value'][0])+'<br>'
                    +'Enrichment second layer=' +str(k['enrichment_value'][1])+'<br>'
                    +'Enrichment third layer=' +str(k['enrichment_value'][2])
                    )

results_df = json_normalize(data=results)

trace1 = go.Scatter3d(
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
        opacity=0.8
    )
)

data = [trace1]
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
                            )
                    )
fig = go.Figure(data=data, layout=layout)
plot(fig,show_link=True,image='png')
