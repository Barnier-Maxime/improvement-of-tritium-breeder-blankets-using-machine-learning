import json
import csv
import pandas as pd

filename  = 'results_point_source/simulation_results_2_layers_halton_first_wall.json'
df = pd.read_json(filename)

df_csv = df.to_csv(index=False)

print (df_csv)