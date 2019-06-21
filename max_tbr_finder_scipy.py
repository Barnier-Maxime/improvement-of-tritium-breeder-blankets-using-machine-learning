
from geometry_breeder_material import *
from scipy import optimize
from noisyopt import minimizeCompass, minimizeSPSA
import numpy as np 
import json 
import json
import pandas as pd
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
from json_file_plot_results import *
import random

def simulate():
    results=[]
    bounds=()
    x0=[]

    with open('results/result_scipy_Li_no_first_wall.json','w') as file_object:
        json.dump([],file_object,indent=2)    

    for number_of_layers in [1,2,3,4]:

        with open('results/result_scipy_Li_no_first_wall.json') as file_object:
            results = json.load(file_object)

        bounds=bounds+(0.0,1.0)
        print(bounds)
        x0.append(0.5)
       
        print(x0)
        result = optimize.minimize(find_tbr, args=[{'material':'Li','firstwall':True,'makeseed':True}],method='Nelder-Mead', x0=x0, bounds=bounds)

        print(result)
        print(1/result.fun)
        json_output = {
                    "max_tbr":1/result.fun,
                    "best_enrichment":list(result.x),
                    "number_of_layers":len(result.x),
                    "breeder_material_name":"Li",
                    "include_firs_wall":False
                    }
        print('json_output',json_output)
        results.append(json_output)

        with open('results/result_scipy_Li_no_first_wall.json','w') as file_object:
            json.dump(results,file_object,indent=2)

def make_plot():
    number_of_layers_plot=[]
    max_tbr_plot=[]
    trace =[]
    df = pd.read_json('results/result_scipy_Li_no_first_wall.json')
    for number_of_layers in [1,2,3,4]:
        
        row_with_number_of_layers = df.loc[df['number_of_layers']==number_of_layers]
        #row_with_max_tbr_number_of_layers = df.loc[row_with_number_of_layers['max_tbr'].idxmax()]

        max_tbr = float(row_with_number_of_layers['max_tbr'])

        # max_tbr_plot.append(max_tbr)

        # PLOTS RESULTS #
        number_of_layers_plot.append(number_of_layers)
        max_tbr_plot.append(max_tbr)
    trace = Scatter(x=number_of_layers_plot, 
                    y=max_tbr_plot,
                    name='Optimized tbr',
                    mode = 'markers+lines',
                    )
    

    layout = {'title':'Optimized max TBR with scipy non uniform enrichment fraction as a function of the number of layer, no first wall and Li',
            'xaxis':{'title':'Number of layer'},
            'yaxis':{'title':'Max TBR'},
            }
    print(trace)
    plot({'data':[trace],
        'layout':layout},
        filename='plots/max_tbr_study_opti_Li_no_first_wall.html')


if __name__ == "__main__":
    simulate()
    # make_plot()