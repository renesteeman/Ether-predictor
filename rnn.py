#RNN

#importing basics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from keras.models import model_from_json
import os

#import training set
#variables
features = 1
training_set = pd.read_csv('data/ethereum.csv')
training_set = training_set.iloc[:, 1:2].values

#keep days_ahead at 20, or bugs may follow (find out why)
days_ahead = 20
days_known = len(training_set)
save_rnn_path = os.path.dirname(os.path.realpath('__file__')) + '\\rnn save\\'
print(save_rnn_path)
RNN = 0


#feature scaling (changing the values to fit in between 0 and 1 so learning'll be faster)
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Creating a data structure with 20 timesteps and t+1 output
x_train = []
y_train = []
#range (days ahead, days in total)
for i in range(days_ahead, days_known):
    x_train.append(training_set_scaled[i-days_ahead:i, 0])
    y_train.append(training_set_scaled[i, 0])
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshaping
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[features], 1))

#building RNN
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


#try to load saved nural net
def load_RNN():
    if Path(save_rnn_path + 'model.json').is_file() and Path(save_rnn_path + 'model.h5').is_file():
        print('found model.json file')
        json_path = save_rnn_path + 'model.json'
        json_file = open(json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        print('Loaded model from disk part 1/2')
        print('found model.h5 file')
        h5_path = save_rnn_path + 'model.h5'
        loaded_model.load_weights(h5_path)
        regressor = loaded_model
        print('Loaded model from disk part 2/2')
        regressor.compile(optimizer = 'rmsprop', loss = 'mean_squared_error')
        global RNN
        RNN = regressor
    else:
        print('model.json file or/and model.h5 file not found, creating RNN')
        create_RNN()

def create_RNN():
    
    #init RNN
    regressor = Sequential()
    
    #adding input and LSTM layers
    regressor.add(LSTM(units = 4, activation = 'sigmoid', input_shape = (None, features)))
    
    #adding output layer
    #change units if output isn't one number
    regressor.add(Dense(units = 1))
    
    #compiling RNN
    #optimizer can be set to adam
    regressor.compile(optimizer = 'rmsprop', loss = 'mean_squared_error')
    
    #fitting the RNN to the training set
    regressor.fit(x_train, y_train, batch_size = 32, epochs = 200)
    
    #save RNN
    print('Saving RNN globally')
    global RNN
    RNN = regressor
    
    save_RNN()

def save_RNN():
    
    print('Saving RNN to disk')
    
    global RNN
    
    # serialize model to JSON
    model_json = RNN.to_json()
    with open(save_rnn_path + 'model.json', 'w') as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    #with open(Path(save_rnn_path + 'model.h5'), 'w') as h5_file:
    #    RNN.save_weights(h5_file)
    RNN.save_weights(save_rnn_path + 'model.h5')
    print('Saved model to disk')

#prepare RNN
load_RNN()

#use RNN

# Making the predictions part 1 (of days now known)
inputs = []
for i in range(days_ahead, days_known):
    inputs.append(training_set_scaled[i-days_ahead:i, 0])
inputs = np.array(inputs)
inputs = np.reshape(inputs, (inputs.shape[0], inputs.shape[1], 1))
predicted_stock_price_train = RNN.predict(inputs)
predicted_stock_price_train = sc.inverse_transform(predicted_stock_price_train)
predicted_stock_price_train = np.concatenate((training_set[0:days_ahead], predicted_stock_price_train), axis = 0)
 

# Making the predictions part 2 (future)
predicted_stock_price_test = []
for i in range(0, days_ahead):
    inputs = []
    for j in range(days_ahead+1+i, days_known+i):
        inputs.append(training_set_scaled[j-days_ahead:j, 0])
    inputs = np.array(inputs)
    inputs = np.reshape(inputs, (inputs.shape[0], inputs.shape[1], 1))
    new_prediction = RNN.predict(inputs)
    predicted_stock_price_test.append(float(new_prediction[len(new_prediction)-1]))
    training_set_scaled = np.concatenate((training_set_scaled, new_prediction[len(new_prediction)-1].reshape(-1,1)), axis = 0)
predicted_stock_price_test = np.array(predicted_stock_price_test).reshape(-1,1)
predicted_stock_price_test = sc.inverse_transform(predicted_stock_price_test)
predicted_stock_price_test = predicted_stock_price_test[1:]
 
#Adding answers together
predicted_stock_price = np.concatenate((predicted_stock_price_train, predicted_stock_price_test), axis = 0)
predicted_stock_price = predicted_stock_price[1:]
predicted_stock_price = predicted_stock_price[-20:]

# Visualising the results
plt.plot(predicted_stock_price, color = 'green', label = 'Predicted Price')
plt.title('Price Predictions')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()




































    



    