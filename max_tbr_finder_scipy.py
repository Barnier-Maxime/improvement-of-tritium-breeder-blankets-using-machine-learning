
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

def simulate():
    results=[]
    bounds=()
    x0=[]

    with open('result_scipy.json','w') as file_object:
        json.dump([],file_object,indent=2)    

    for number_of_layers in [1,2,3,4,5,6]:

        with open('result_scipy.json') as file_object:
            results = json.load(file_object)

        bounds=bounds+((0.0,1.0),)
        print(bounds)
        x0.append(0.5)
        x=np.asarray(x0)
        print(x0)
        result = optimize.minimize(find_tbr, x0=x0, bounds=bounds)

        print(result)
        print(1/result.fun)
        json_output = {
                    "max_tbr":1/result.fun,
                    "best_enrichment":list(result.x),
                    "number_of_layers":len(result.x)
                    }
        print('json_output',json_output)
        results.append(json_output)

        with open('result_scipy.json','w') as file_object:
            json.dump(results,file_object,indent=2)

def make_plot():
    number_of_layers_plot=[]
    max_tbr_plot=[]
    trace =[]
    df = pd.read_json('result.json')
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
    

    layout = {'title':'Optimized max TBR with non uniform enrichment fraction as a function of the number of layer',
            'xaxis':{'title':'Number of layer'},
            'yaxis':{'title':'Max TBR'},
            }
    print(trace)
    plot({'data':[trace],
        'layout':layout},
        filename='max_tbr_study_opti.html')


if __name__ == "__main__":
    #simulate()
    make_plot()