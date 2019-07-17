# example of making predictions for a regression problem
# from https://machinelearningmastery.com/how-to-make-classification-and-regression-predictions-for-deep-learning-models-in-keras/
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
# generate regression dataset
filename = 'results_point_source/simulation_results_2_layers_halton_first_wall.json'
df = pd.read_json(filename)
df_filtered = df.loc[(df['breeder_material_name']=='Li')]
answer = list(df_filtered['value'])[0]
X = np.array(list(df_filtered['enrichment_value']))
y = np.array(list(df_filtered['value']))

scalarX, scalarY = MinMaxScaler(), MinMaxScaler()
#scalarX.fit(X)
scalarY.fit(y.reshape(len(y),1))
#X = scalarX.transform(X)
y = scalarY.transform(y.reshape(len(y),1))
# define and fit the final model
# model = Sequential()
# model.add(Dense(64, input_dim=len(X[0]), activation='relu'))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(1, activation='relu'))
# model.compile(loss='mse', optimizer=tf.keras.optimizers.SGD(0.001))
# model.fit(X, y, epochs=1000, verbose=0)
# new instances where we do not know the answer

model = keras.Sequential([
    layers.Dense(32, activation = tf.keras.activations.sigmoid, input_shape = [len(X[0])]),
    layers.Dense(32, activation = tf.keras.activations.sigmoid),
    layers.Dense(64, activation = tf.keras.activations.sigmoid),
    layers.Dense(128, activation = tf.keras.activations.linear),
    layers.Dense(64, activation = tf.keras.activations.linear),
    layers.Dense(32, activation = tf.keras.activations.linear),
    #layers.Dense(32, activation = tf.keras.activations.linear),
    #layers.Dense(128, activation = tf.keras.activations.linear),
    layers.Dense(1, activation = tf.keras.activations.linear)
])

#optimizer = tf.keras.optimizers.SGD(0.01) #stochastic gradient descent : up to 0.95
#optimizer = tf.keras.optimizers.RMSprop(0.0001) #up to 0.93
#optimizer = tf.keras.optimizers.Adagrad(0.1) #up to 0.94
optimizer = tf.keras.optimizers.Adadelta(1) #up to 0.952
#optimizer = tf.keras.optimizers.Adam(0.0001) #up to 0.94
#optimizer = tf.keras.optimizers.Adamax(0.1) #up to 0.95
#optimizer = tf.keras.optimizers.Nadam(0.001)

model.compile(
    loss = 'mean_squared_error',
    optimizer = optimizer,
    metrics =['mean_squared_error']
)

model.fit(X, y, epochs=1000, batch_size = 64, verbose=0)

# Xnew, a = make_regression(n_samples=3, n_features=2, noise=0.1, random_state=1)
enrichment_fractions = list(df_filtered['enrichment_value'])[0]
Xnew = np.array([enrichment_fractions])
print('answer is', answer)

#Xnew = scalarX.transform(Xnew)
# make a prediction
ynew = model.predict(Xnew)
scalarY.fit(ynew.reshape(len(ynew),1))
#ynew = scalarY.transform(ynew.reshape(len(ynew),1))
ynew = scalarY.inverse_transform(ynew)
# show the inputs and predicted outputs
for i in range(len(Xnew)):
	print("X=%s, Predicted=%s" % (Xnew[i], ynew[i]))