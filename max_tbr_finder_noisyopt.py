
from geometry_breeder_material import *
from noisyopt import minimizeCompass, minimizeSPSA
import numpy as np 
import json 

results=[]

for number_of_layers in [1,2,3,4,5,6]:

    bounds =np.array([[0.0,1.0] for k in range(number_of_layers)])
    x0=np.array([[0.5] for k in range(number_of_layers)])


    result = minimizeCompass(find_tbr_with_seed, bounds=bounds, x0=x0, deltatol=0.01, disp=True, paired=True)
    # result = minimizeSPSA(find_tbr, bounds=bounds, x0=x0, paired=False, disp=True)

    print(result)
    print(1/result.fun)

    results.append({
                    "max_tbr":1/result.fun,
                    "best_enrichment":result.x,
                    "number_of_layers":len(result.x)
                    })

with open('result.json','w') as f:
    json.dump(results,f)
