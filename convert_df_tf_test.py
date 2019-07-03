import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn import preprocessing

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

def find_prediction(filename, material, enrichment_first_layer, enrichment_second_layer, enrichment_third_layer, enrichment_fourth_layer, TBR_values):
    
    df = pd.read_json(filename)
    df_filtered = df.loc[df['breeder_material_name']==material]

    x = TBR_values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    print('x_scaled', x_scaled)
    # TBR_values = df_filtered['value'].tolist()
    
    dataset = pd.DataFrame({
        'enrichment_first_layer':enrichment_first_layer,
        'enrichment_second_layer':enrichment_second_layer,
        'enrichment_third_layer':enrichment_third_layer,
        'enrichment_fourth_layer':enrichment_fourth_layer,
        'TBR_values':x_scaled[0][0] #normed TBR values between 0 and 1
    })

    test_dataset = dataset

    model = build_model(test_dataset)
    model.summary()

    df_prediction = pd.DataFrame({
        'enrichment_first_layer':enrichment_first_layer,
        'enrichment_second_layer':enrichment_second_layer,
        'enrichment_third_layer':enrichment_third_layer,
        'enrichment_fourth_layer':enrichment_fourth_layer,
        'TBR_values':TBR_values
    })

    print('enrichment_first_layer', enrichment_first_layer)
    print('enrichment_second_layer', enrichment_second_layer)
    print('enrichment_third_layer', enrichment_third_layer)
    print('enrichment_fourth_layer', enrichment_fourth_layer)
    print('TBR_values', TBR_values)

    test_labels = test_dataset.pop('TBR_values') #only TBR values of the test

    print('test_labels',test_labels)


    prediction_labels = df_prediction.pop('TBR_values') #only TBR value for the prediction
    result = model.predict(df_prediction) #list of list with one prediction on the df_prediction


    test_predictions = model.predict(test_dataset) #list of list with all the normed TBR predicted from test_dataset
    loss, mae, mse = model.evaluate(test_dataset, test_labels, verbose=0)

    test_predictions = min_max_scaler.inverse_transform(test_predictions)

    print('TBR_predictions_jon_method', test_predictions[0][0])
    print('Reverse_TBR_prediction', 1/test_predictions[0][0])


    return(1/test_predictions[0][0])
    

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
    find_prediction('results_point_source/simulation_results_4_layers_halton_first_wall.json','Li', 0.5, 0.5, 0.5, 0.5, [[1.1]])
