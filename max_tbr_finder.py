
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout

# normalized_df = json_normalize(df['enrichment_value'])

x=[]
y_non_uniform=[]
y_uniform=[]
number_max_of_layers=8

for k in range(1,number_max_of_layers+1):
      df = pd.read_json('simulation_results_'+str(k)+'_layers_non_uni.json') 

      row_with_max_tbr = df.loc[df['value'].idxmax()] 
      max_tbr = row_with_max_tbr['value']
      enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
      x.append(k)
      y_non_uniform.append(max_tbr)

      df = pd.read_json('simulation_results_'+str(k)+'_layers_uni.json') 

      row_with_max_tbr = df.loc[df['value'].idxmax()] 
      max_tbr = row_with_max_tbr['value']
      enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
      y_uniform.append(max_tbr)

# PLOTS RESULTS #
non_uniform_enrichment= Scatter(x=x, 
                y=y_non_uniform,
                mode = 'lines',
                )
uniform_enrichment= Scatter(x=x, 
                y=y_uniform,
                mode = 'lines',
                )               

layout = {'title':'Max TBR with uniform and non uniform enrichment fraction as a function of the number of layer',
          'xaxis':{'title':'Number of layer'},
          'yaxis':{'title':'Max TBR'},
         }
plot({'data':[non_uniform_enrichment,uniform_enrichment],
      'layout':layout},
      filename='max_tbr_study.html')

