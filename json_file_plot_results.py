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

with open('simulation_results_old.json') as f:
    results = json.load(f)

# PLOTS RESULTS #
x_axis = []
y_axis = []
z_axis = []
TBR = []
#print(results)
for k in range(len(results)): # creation of the 3 axis
    x_axis.append(results[k]['enrichment_value'][0])
    y_axis.append(results[k]['enrichment_value'][1])
    z_axis.append(results[k]['enrichment_value'][2])
    TBR.append(results[k]['value'])

results_df = json_normalize(data=results)

#fig = plt.figure()

#ax = fig.add_subplot(111, projection='3d')
#pnt3d=ax.scatter(x_axis,y_axis,z_axis,c=TBR)
#cbar=plt.colorbar(pnt3d)
#cbar.set_label("TBR value")
#ax.set_xlabel('enrichment first layer')
#ax.set_ylabel('enrichment second layer')
#ax.set_zlabel('enrichment third layer')

#plt.show()

trace1 = go.Scatter3d(
    x=x_axis,
    y=y_axis,
    z=z_axis,
    mode='markers',
    marker=dict(
        size=5,
        color=TBR,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)

data = [trace1]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=data, layout=layout)
plot(fig,show_link=False)




# traces = {}
# x_axis_name='enrichment'
# traces[x_axis_name]=[]
# for material_name in all_materials:

#             df_filtered_by_mat = results_df[results_df['breeder_material_name']==material_name]

#             tally = df_filtered_by_mat[tally_name+'.value']
#             tally_std_dev = df_filtered_by_mat[tally_name+'.std_dev']

#             traces[x_axis_name].append(Scatter(x=df_filtered_by_mat[x_axis_name], 
#                                     y= tally,
#                                     mode = 'markers',                   
#                                     name = material_name,                
#                                     error_y= {'array':tally_std_dev},
#                                     )
#                                 )
# layout_ef = {'title':tally_name+' and '+x_axis_name,
#                     'hovermode':'closest',
#             'xaxis':{'title':x_axis_name},
#             'yaxis':{'title':tally_name},
#             }
# plot({'data':traces[x_axis_name],
#     'layout':layout_ef},
#     filename=tally_name+'_vs_'+x_axis_name+'.html'
#     )
