import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

def convert_df_in_tf(filename, material):
    df=pd.read_json(filename)
    df_filtered = df.loc[(df['breeder_material_name']==material)]
    tf.enable_eager_execution()
    dataset = (  
         tf.data.Dataset.from_tensor_slices(  
                    (  
                      tf.cast(list(df_filtered['enrichment_value']), tf.float32),  
                      tf.cast(df_filtered['std_dev'].values,tf.float32), 
                      tf.cast(df_filtered['value'].values, tf.float32)  
                    )  
                )  
            ) 
    for enrichment_value, std_dev, value in dataset : 
        print(f'enrichment_value:{enrichment_value} Std_dev:{std_dev} TBR:{value}') 
    
    return(dataset)
   
def find_prediction(filename):
    df = pd.read_json(filename)
    df.isna().sum()
    df = df.dropna()
    train_df = df.sample(frac=0.8, random_state=0)
    test_df = df.drop(train_df.index)
    L = list(test_df['value'])
    M = list(test_df['std_dev'])
    train_labels = train_df.pop('value')
    test_labels = test_df.pop('value')

    def build_model():
        model = keras.Sequential([
            layers.Dense(64, activation = tf.nn.relu, input_shape = [1]),
            layers.Dense(64, activation = tf.nn.relu),
            layers.Dense(1)
        ])
        optimizer = tf.keras.optimizers.RMSprop(0.001)

        model.compile(
            loss = 'mean_squared_error',
            optimizer = optimizer,
            metrics = ['mean_absolute_error','mean_squared_error']
        )
        return(model)
    model = build_model()

    batch = test_labels
    #print(batch)
    #result = model.predict(batch)
    #print(result)
    test_predictions = model.predict(batch).flatten()
    print(test_predictions)
    test_predictions_real=[]
    
    for k in range(len(test_predictions)):
        std_dev = M[k]
        value = L[k]
        test_predictions_real.append(test_predictions[k]*std_dev+value)

    plt.scatter(batch,test_predictions_real)
    plt.xlabel('True Values [TBR]')
    plt.ylabel('Predictions [TBR]')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0.5,plt.xlim()[1]])
    plt.ylim([0.5,plt.ylim()[1]])
    _=plt.plot([-2,2], [-2,2])
    plt.show()

if __name__== '__main__':
    find_prediction('results_point_source/simulation_results_4_layers_halton_first_wall.json')

    
