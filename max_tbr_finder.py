
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

# 1 LAYER
df = pd.read_json('simulation_results_1_layer_non_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
x.append(1)
y_non_uniform.append(max_tbr)
y_uniform.append(max_tbr) #max TBR are calculated for 1000 simulations

#df['enrichment_value.1']


#2 LAYERS
df = pd.read_json('simulation_results_2_layers_non_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
x.append(2)
y_non_uniform.append(max_tbr)

df = pd.read_json('simulation_results_2_layers_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
y_uniform.append(max_tbr)

#3 LAYERS
df = pd.read_json('simulation_results_3_layers_non_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
x.append(3)
y_non_uniform.append(max_tbr)

df = pd.read_json('simulation_results_3_layer_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
y_uniform.append(max_tbr)

#4 LAYERS
df = pd.read_json('simulation_results_4_layers_non_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
x.append(4)
y_non_uniform.append(max_tbr)

df = pd.read_json('simulation_results_4_layers_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
y_uniform.append(max_tbr)

#5 LAYERS
df = pd.read_json('simulation_results_5_layers_non_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
x.append(5)
y_non_uniform.append(max_tbr)

df = pd.read_json('simulation_results_5_layers_uni.json') #check

row_with_max_tbr = df.loc[df['value'].idxmax()] 
max_tbr = row_with_max_tbr['value']
enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
print(row_with_max_tbr)
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

