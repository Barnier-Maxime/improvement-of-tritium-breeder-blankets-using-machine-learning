from geometry_breeder_material import *
#from max_tbr_finder import *
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
import numpy as np

# normalized_df = json_normalize(df['enrichment_value'])



number_max_of_layers=5


for k in range(1,number_max_of_layers+1):
    df = pd.read_json('simulation_results_'+str(k)+'_layers_uni.json') 
    row_with_max_tbr = df.loc[df['value'].idxmax()] 
    
    enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
    y_uniform=enrichment_at_max_tbr
    radius=[i*100/k for i in range(1,number_max_of_layers+1)]

    df = pd.read_json('simulation_results_'+str(k)+'_layers_non_uni.json') 
    row_with_max_tbr = df.loc[df['value'].idxmax()] 
    enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
    y_non_uniform=enrichment_at_max_tbr


# PLOTS RESULTS #
non_uniform_enrichment_layer= Scatter(x=radius, 
                y=y_non_uniform,
                name='Non uniform enrichment',
                mode = 'markers',
                marker=dict(
                            size = 10,
                            color = 'rgba(255,182,193,.9)',
                            line = dict(
                                        width = 2,
                                        color = 'rgb(0,0,0)'
                                    )

                        )
                        )
                        

uniform_enrichment_layer= Scatter(x=radius, 
                y=y_uniform,
                mode = 'markers',
                name='Uniform enrichment',
                marker=dict(
                            size = 10,
                            color = 'rgba(152,0,0,.8)',
                            line = dict(
                                        width = 2,
                                        color = 'rgb(0,0,0)'
                                    )

                        )
                    )

layout = {'title':'Enrichment fractions in Li6 as a function of the radius',
        'xaxis':{'title':'Radius in cm'},
        'yaxis':{'title':'Enrichment fraction in Li6'},
        }
plot({'data':[non_uniform_enrichment_layer,uniform_enrichment_layer],
    'layout':layout},
    filename='enrichment_with_radius_layer_'+str(k)+'.html')