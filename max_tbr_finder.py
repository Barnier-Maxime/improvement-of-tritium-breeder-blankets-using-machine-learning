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

#print(results[0]['value'])
values=[]
for k in range(len(results)):
    values.append(results[k]['value'])
max_TBR=max(values)
print(max_TBR)

indice=0

for j in range(len(results)):
    if results[j]['value']==max_TBR:
        indice+=j
    else:
        indice=indice

optimum_enrichment=results[j]['enrichment_value']
print(optimum_enrichment)

