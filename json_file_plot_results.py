import openmc
import os
import json
import numpy as np
from numpy import random
import re 
from tqdm import tqdm

from material_maker_functions import *

from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter3d, Layout, Scatter
import pandas as pd
from pandas.io.json import json_normalize

with open('simulation_results_old.json') as f:
    results = json.load(f)

# PLOTS RESULTS #

print(results[0]['enrichment_value'][0])
print(results[0]['enrichment_value'][1])
print(results[0]['enrichment_value'][2])
print(results[0]['value'])

# results_df = json_normalize(data=results)


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