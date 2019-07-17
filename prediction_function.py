from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json
from geometry_breeder_material import *
from scipy.optimize import minimize

def build_model(filename, material):
    openfile = open(filename)
    jsondata = json.load(openfile)
    df = pd.DataFrame(jsondata)
    #df = pd.read_json(filename)
    df_filtered = df.loc[(df['breeder_material_name']==material)]
    #answer = list(df_filtered['value'])[0]
    X = np.array(list(df_filtered['enrichment_value']))

    model = keras.Sequential([
    layers.Dense(8, activation = tf.keras.activations.linear, input_shape = [len(X[0])]),
    #layers.Dense(32, activation = tf.keras.activations.sigmoid),
    layers.Dense(16, activation = tf.keras.activations.tanh),
    layers.Dense(16, activation = tf.keras.activations.sigmoid),
    #layers.Dense(16, activation = tf.keras.activations.tanh),
    layers.Dense(32, activation = tf.keras.activations.sigmoid),
    #layers.Dense(512, activation = tf.keras.activations.sigmoid),
    #layers.Dense(256, activation = tf.keras.activations.sigmoid),
    layers.Dense(64, activation = tf.keras.activations.sigmoid),
    layers.Dense(64, activation = tf.keras.activations.sigmoid),
    layers.Dense(32, activation = tf.keras.activations.sigmoid),
    #layers.Dense(32, activation = tf.keras.activations.sigmoid),
    layers.Dense(16, activation = tf.keras.activations.sigmoid),
    layers.Dense(8, activation = tf.keras.activations.sigmoid),
    layers.Dense(1, activation = tf.keras.activations.linear)
    ])

    optimizer = tf.keras.optimizers.Adadelta(1)

    model.compile(
        loss = 'mean_squared_error',
        optimizer = optimizer,
        metrics =['mean_squared_error']
        )
    return(model)

def make_prediction(filename, material):
    openfile = open(filename)
    jsondata = json.load(openfile)
    df = pd.DataFrame(jsondata)
    #df = pd.read_json(filename)
    df_filtered = df.loc[(df['breeder_material_name']==material)]
    answer = list(df_filtered['value'])[0]
    X = np.array(list(df_filtered['enrichment_value']))
    y = np.array(list(df_filtered['value']))

    scalarX, scalarY = MinMaxScaler(), MinMaxScaler()
    scalarY.fit(y.reshape(len(y),1))
    y = scalarY.transform(y.reshape(len(y),1))

    model = build_model(filename, material)
    model.fit(X, y, epochs=1000, batch_size = 8, verbose=0)

    enrichment_fractions = list(df_filtered['enrichment_value'])[0]
    Xnew = np.array([enrichment_fractions])
    print('answer is', answer)
    ynew = model.predict(Xnew)
    scalarY.fit(ynew.reshape(len(ynew),1))
    ynew = scalarY.inverse_transform(ynew)

    for i in range(len(Xnew)):
	    print("X=%s, Predicted=%s, Difference=%s" % (Xnew[i], ynew[i], ynew[i]-answer))

    return(1/ynew[0])

def model(enrichment_fractions, material, filename):
    Xnew = np.array([enrichment_fractions])
    model = build_model(filename, material)
    ynew = model.predict(Xnew)
    scalarY = MinMaxScaler()
    scalarY.fit(ynew.reshape(len(ynew),1))
    ynew = scalarY.inverse_transform(ynew)
    return (1/ynew)

def optimizer_enrcihment_fraction(filename, material):
    openfile = open(filename)
    jsondata = json.load(openfile)
    df = pd.DataFrame(jsondata)
    #df = pd.read_json(filename)
    df_filtered = df.loc[(df['breeder_material_name']==material)]
    output = []
    results = []
    bounds = ()
    x0 = []
    for k in range (len(list(df_filtered['enrichment_value'])[0])):
        x0.append(0.5)
        bounds = bounds + ((0,1),)  #WARNING : must modify find_tbr function 
                                    #in geometry_breeder_material : specify 
                                    #the material, nps, batches 
    print(x0)
    result = minimize(model, x0=x0, args=(material, filename), method='TNC', bounds=bounds)
    results.append(result.x)
    output.append(results)
    output.append(1/result.fun)
    json_output = {'first_wall':True,
                    'number_of_materials':len(list(df_filtered['enrichment_value'])[0]),
                    'graded':'graded',
                    'enrichment_value':list(output[0][0]),
                    'value':output[1][0][0],
                    'std_dev':'not given by noisyopt',
                    'breeder_material_name':material,
                    'nps':int(list(df_filtered['nps'])[0])
    }

    print('json_ouput', json_output)
    
    input()
    
    # with open(filename, 'w') as file_object:
    #     json.dump(json_output, file_object, indent=2)

    # return(json_output)

if __name__== '__main__':
    filename = 'results_new_neutron_source/simulation_results_2_layers_halton_first_wall_neural_network.json'
    material = 'Li'
    for k in range(5):
        make_prediction(filename, material)
    optimizer_enrcihment_fraction(filename, material)