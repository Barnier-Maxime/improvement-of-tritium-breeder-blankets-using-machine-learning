import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn import preprocessing
from noisyopt import minimizeCompass, minimizeSPSA
import json


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

def build_model(train_dataset):
    model = keras.Sequential([
        layers.Dense(64, activation = tf.nn.relu, input_shape = [len(train_dataset.keys())]),
        layers.Dense(64, activation = tf.nn.relu),
        layers.Dense(1)
    ])
    #optimizer = tf.keras.optimizers.RMSprop(0.001)
    optimizer = tf.keras.optimizers.SGD(0.001) #stochastic gradient descent 

    model.compile(
        loss = 'mean_squared_error',
        optimizer = optimizer,
        metrics = ['mean_absolute_error','mean_squared_error']
    )
    return(model)

def find_prediction(enrichment_fractions, filename, material, TBR_values):
    #filename = 'results_point_source/simulation_results_4_layers_halton_first_wall.json'
    #material = 'Li'
    results_prediction = []
    with open('results_new_neutron_source/result_prediction_'+str(material)+'_'+str(True)+'.json','w') as file_object:
        json.dump([],file_object,indent=2)  

    df = pd.read_json(filename)
    df_filtered = df.loc[df['breeder_material_name']==material]

    x_dataset = df_filtered[['value']].values.astype(float)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled_dataset = min_max_scaler.fit_transform(x_dataset)

    x = TBR_values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)

    enrichment_first_layer_dataset = [item[0] for item in df_filtered['enrichment_value'].tolist()]
    enrichment_second_layer_dataset = [item[1] for item in df_filtered['enrichment_value'].tolist()]
    enrichment_third_layer_dataset = [item[2] for item in df_filtered['enrichment_value'].tolist()]
    enrichment_fourth_layer_dataset = [item[3] for item in df_filtered['enrichment_value'].tolist()]
    # TBR_values = df_filtered['value'].tolist()
    TBR_values_dataset = []
    for i in x_scaled_dataset:
        TBR_values_dataset.append(i[0])

    dataset = pd.DataFrame({
        'enrichment_first_layer':enrichment_first_layer_dataset,
        'enrichment_second_layer':enrichment_second_layer_dataset,
        'enrichment_third_layer':enrichment_third_layer_dataset,
        'enrichment_fourth_layer':enrichment_fourth_layer_dataset,
        'TBR_values':TBR_values_dataset #normed TBR values between 0 and 1
    })

    train_dataset = dataset.sample(frac=(len(df_filtered['value'])-1)/len(df_filtered['value']), random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_labels = train_dataset.pop('TBR_values')
    model = build_model(train_dataset)
    model.summary()

    df_prediction = pd.DataFrame({
        'enrichment_first_layer':enrichment_fractions[0],
        'enrichment_second_layer':enrichment_fractions[1],
        'enrichment_third_layer':enrichment_fractions[2],
        'enrichment_fourth_layer':enrichment_fractions[3],
        'TBR_values':TBR_values
    })
    
    print('enrichment_first_layer', enrichment_fractions[0])
    print('enrichment_second_layer',enrichment_fractions[1])
    print('enrichment_third_layer', enrichment_fractions[2])
    print('enrichment_fourth_layer', enrichment_fractions[3])
    print('TBR_values', TBR_values)
    
    test_labels = test_dataset.pop('TBR_values') #only TBR values of the test

    print('test_labels',test_labels)

    prediction_labels = df_prediction.pop('TBR_values') #only TBR value for the prediction
    result = model.predict(df_prediction) #list of list with one prediction on the df_prediction
    result = min_max_scaler.inverse_transform(result) #TBR prediction with the enrichment in argument and the tbr
    
    result_prediction = {
        'first_wall' : True,
        'number_of_materials' : int(df_filtered[['number_of_materials']].values.astype(int)[0]),
        'graded' : 'graded',
        'enrichment_value' : [
            enrichment_fractions[0],
            enrichment_fractions[1],
            enrichment_fractions[2],
            enrichment_fractions[3]
        ],
        'TBR_values' : result[0][0],
        'breeder_material_name' : material,
    } 
    results_prediction.append(result_prediction)
    print('result', result[0][0])
    input()
    with open('results_new_neutron_source/result_prediction_'+str(material)+'_'+str(True)+'.json','w') as file_object:
        json.dump(results_prediction,file_object,indent=2)
    
    print('json', json)

    test_predictions = model.predict(test_dataset) #list of list with all the normed TBR predicted from test_dataset
    loss, mae, mse = model.evaluate(test_dataset, test_labels, verbose=0)

    test_predictions = min_max_scaler.inverse_transform(test_predictions) #tbr prediction on the dataset with the random sample in the df

    # print('TBR_predictions_jon_method', test_predictions[0][0])
    # print('Reverse_TBR_prediction', 1/test_predictions[0][0])

    return(1/result_prediction['TBR_values'])

    # input()
    # test_labels = test_dataset.pop('TBR_values') #only TBR values of the test
    # test_labels = test_dataset

    # print('test_labels',test_labels)

    # prediction_labels = df_prediction.pop('TBR_values') #only TBR value for the prediction
    # print('df_prediction', df_prediction)
    # result = model.predict(df_prediction) #list of list with one prediction on the df_prediction
    # print('result', result)
    # test_predictions = model.predict(test_dataset) #list of list with all the normed TBR predicted from test_dataset
    # #loss, mae, mse = model.evaluate(test_dataset, test_labels, verbose=0)

    # test_predictions = min_max_scaler.inverse_transform(test_predictions)

    # print('TBR_predictions_max_method', test_predictions[0][0])

# print('test_labels',type(test_labels.tolist()))
# test_labels_stripped = test_labels.tolist()

# print('test_labels',test_labels_stripped)


# test_labels_stripped = min_max_scaler.inverse_transform(test_labels_stripped)


# plt.scatter(test_labels_stripped,test_predictions)
# plt.xlabel('True TBR')
# plt.ylabel('Predicted TBR')
# plt.show()

    # input()

    # batch = test_labels
    # #print(batch)

    # test_predictions = model.predict(batch).flatten()
    # print(test_predictions)
    
    # plt.scatter(batch,test_predictions)
    # plt.xlabel('True Values [TBR]')
    # plt.ylabel('Predictions [TBR]')
    # plt.axis('equal')
    # plt.axis('square')
    # plt.xlim([0.5,plt.xlim()[1]])
    # plt.ylim([0.5,plt.ylim()[1]])
    # _=plt.plot([-2,2], [-2,2])
    # plt.show()

    # #finding the error (should be like a gaussian)
    # error = test_predictions - test_labels
    # plt.hist(error, bins = 25)
    # plt.xlabel('Prediction error [TBR]')
    # _ = plt.ylabel('count')
    # plt.show()
    # print(max(test_predictions))


if __name__== '__main__':
    # filename = 'results_point_source/simulation_results_4_layers_halton_first_wall.json'
    # material = 'Li'
    # find_prediction(filename,material)
    find_prediction([0.5,0.5,0.5,0.5], 'results_point_source/simulation_results_4_layers_halton_first_wall.json','Li', [[1.1]])
