
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
eps=1e-5

for k in range(1,number_max_of_layers+1):
    #   df = pd.read_json('simulation_results_'+str(k)+'_layers_uni.json') 
    #   row_with_max_tbr = df.loc[df['value'].idxmax()] 
    #   max_tbr = row_with_max_tbr['value']
    #   std_dev_uni.append(row_with_max_tbr['std_dev'])
    #   enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
    #   y_uniform.append(max_tbr)

      df = pd.read_json('simulation_results_'+str(k)+'_layers_non_uni.json') 
      print(df)
      row_with_max_tbr = df.loc[df['value'].idxmax()] 
      max_tbr = row_with_max_tbr['value']
      std_dev_non_uni.append(row_with_max_tbr['std_dev'])
      enrichment_at_max_tbr = row_with_max_tbr['enrichment_value']
      x.append(k)
      y_non_uniform.append(max_tbr)

      x_gradient_descent=[df['enrichment_value']] #serie containing all the enrichment values for each simulation with k layers
      y_gradient_descent=[df['value']] #serie containing all the tbr for each simulation with k layers
      list_of_tbr=list(y_gradient_descent[0]) # list of all tbr with k layers for each simulation
      list_of_enrichments=list(x_gradient_descent[0]) #list of all enrichments for k layers for each simulation
      list_of_tbr.remove(max_tbr)
      second_highest_tbr = max(list_of_tbr)
      index_second_highest_tbr=df.loc[df['value']==second_highest_tbr].index[0]
      print(index_second_highest_tbr)
      enrichment_second_highest_tbr=df.enrichment_value[index_second_highest_tbr]
      print(enrichment_second_highest_tbr)

      module_gradient_square=0
      x0 = [] #enrichment values for the calulation of the gradient
      for i in range(number_max_of_layers):
            y0=np.array([max_tbr,second_highest_tbr])
            x0.append([enrichment_at_max_tbr[i],enrichment_second_highest_tbr[i]]) #enrichment for the higher and the second higher tbr in the layer i
            module_gradient_square+=((np.gradient(y0,x0[i])))**2
      if (module_gradient_square)**(1/2)>eps:
            j=0 
            for coord in x0: 
                coord+=0.01*np.gradient(np.array(y0[j]),coord)
                j=1 
                print(x0)


      
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
