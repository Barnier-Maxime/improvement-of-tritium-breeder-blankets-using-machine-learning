
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
import numpy as np

# normalized_df = json_normalize(df['enrichment_value'])

x=[]
y_non_uniform=[]
y_uniform=[]
number_max_of_layers=3
std_dev_non_uni=[]
std_dev_uni=[]

for k in range(1,number_max_of_layers+1):
      df = pd.read_json('simulation_results_'+str(k)+'_layers_uni.json') 
      row_with_max_tbr = df.loc[df['value'].idxmax()] 
      max_tbr = row_with_max_tbr['value']
      std_dev_uni.append(row_with_max_tbr['std_dev'])
      enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
      y_uniform.append(max_tbr)

      df = pd.read_json('simulation_results_'+str(k)+'_layers_non_uni.json') 
      print(df)
      row_with_max_tbr = df.loc[df['value'].idxmax()] 
      max_tbr = row_with_max_tbr['value']
      std_dev_non_uni.append(row_with_max_tbr['std_dev'])
      enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
      x.append(k)
      y_non_uniform.append(max_tbr)
  
print(std_dev_non_uni)
print(std_dev_uni)

# PLOTS RESULTS #
non_uniform_enrichment= Scatter(x=x, 
                y=y_non_uniform,
                name='Non uniform enrichment',
                mode = 'lines',
                error_y=dict(type='data',
                              array=std_dev_uni,
                              visible=True
                )
                )

uniform_enrichment= Scatter(x=x, 
                y=y_uniform,
                mode = 'lines',
                name='Uniform enrichment',
                error_y=dict(type='data',
                              array=std_dev_non_uni,
                              visible=True
                )
            )

layout = {'title':'Max TBR with uniform and non uniform enrichment fraction as a function of the number of layer',
          'xaxis':{'title':'Number of layer'},
          'yaxis':{'title':'Max TBR'},
         }
plot({'data':[non_uniform_enrichment,uniform_enrichment],
      'layout':layout},
      filename='max_tbr_study.html')
