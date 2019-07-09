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

df = pd.read_json('results_point_source/simulation_results_4_layers_halton_first_wall.json')
df_filtered = df.loc[(df['breeder_material_name']=='Li')]

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
    layers.Dense(64, activation = tf.nn.relu, input_shape = [len(X[0])]),
    layers.Dense(64, activation = tf.nn.relu),
    layers.Dense(1)
])

#optimizer = tf.keras.optimizers.SGD(0.1) #stochastic gradient descent : up to 0.95
#optimizer = tf.keras.optimizers.RMSprop(0.01) #up to 0.93
#optimizer = tf.keras.optimizers.Adagrad(0.1) #up to 0.94
#optimizer = tf.keras.optimizers.Adadelta(2) #up to 0.952
#optimizer = tf.keras.optimizers.Adam(0.0001) #up to 0.94
#optimizer = tf.keras.optimizers.Adamax(0.1) #up to 0.95
optimizer = tf.keras.optimizers.Nadam(0.001)

model.compile(
    loss = 'mean_squared_logarithmic_error',
    optimizer = optimizer,
    metrics = ['accuracy']#['mean_absolute_error','mean_squared_error']
)

model.fit(X, y, epochs=1000, verbose=0)

# Xnew, a = make_regression(n_samples=3, n_features=2, noise=0.1, random_state=1)
Xnew = np.array([[0.75,0.1111111111111111,0.6,0.428571428571428550]])
#answer is 1.2516885096999306

#Xnew = scalarX.transform(Xnew)
# make a prediction
ynew = model.predict(Xnew)
scalarY.fit(ynew.reshape(len(ynew),1))
#ynew = scalarY.transform(ynew.reshape(len(ynew),1))
ynew = scalarY.inverse_transform(ynew)
# show the inputs and predicted outputs
for i in range(len(Xnew)):
	print("X=%s, Predicted=%s" % (Xnew[i], ynew[i]))