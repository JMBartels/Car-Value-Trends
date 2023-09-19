# -*- coding: utf-8 -*-
"""
@author: jbartels
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def limit(num,minimum=0):
    if num <= minimum:
        return minimum
    else:
        return num

def simulate_film(MW,th_init,conc):
    k= 5E5
    t_half = 20
    UCL = 0.06
    LED = 0.013
    Rd = k*MW**(-3/2) 
    Current_conc = 0
    
    th_all = []
    conc_all = [0]
    
    
    t_length = 2001
    t = np.arange(0,t_length)
    UCL = 0.06
    LED = [0.013]*t_length

    
    for i in range(len(t)):
        if i == 0:
            th_now = th_init
            th_prev = th_now
            th_all.append(th_now)

        else:
            th_now = limit(th_init - Rd*t[i]) #remove th by rate, determined by MW

            th_all.append(th_now) #make a list of th at each t

            loss_to_conc = Current_conc*(1/2)**((1)/t_half) # using (1) as the time step dt

            Current_conc = loss_to_conc
            Current_conc = Current_conc + (th_prev-th_now)*conc #add conc from dissolved polymer
            conc_all.append(Current_conc)
            th_prev = th_now
        
    Above_LED = np.subtract(np.array(conc_all), np.array(LED))
    firstIndex = next((index for index, value in enumerate(Above_LED) if value > 0), -1) #find index of first time conc becomes effective
    lastIndex = t_length - next((index for index, value in enumerate(reversed(Above_LED)) if value > 0), -1) #find index when conc stops being effective

    time_to_active = firstIndex #currently estimate by the hour
    time_spent_active = round((lastIndex - firstIndex)/24,2) #time in days

    if np.max(conc_all) > UCL:
        is_safe = False
    else:
        is_safe = True


    return is_safe, time_to_active, time_spent_active


#########
#generate a sample database
#set n number of samples
#iterate n times, generate MW,th,conc randomly between values
#simulate the sample, then store output metrics as targets

num_samples = 2000
features = [] #MW, th, conc
targets = [] #is_safe, time_to_active, time_spent_active

print('Generating simulated database...')

for i in range(num_samples):
    #generate a random sample in a reasonable range
    temp_MW = np.random.randint(10000,500000)
    temp_th = np.random.randint(1,300)/100
    temp_conc = np.random.randint(5,300)/100
    
    temp_input = np.array([temp_MW, temp_th, temp_conc])
    
    
    #simulate the sample
    temp_is_safe, temp_time_to_active, temp_time_spent_active = simulate_film(temp_MW, temp_th, temp_conc)
    if temp_time_to_active > 0:
        features.append(temp_input)
        temp_result = np.array([temp_is_safe, temp_time_to_active, temp_time_spent_active])
        targets.append(temp_result)
    else:
        pass


######
#Make a neural  network with 2 dense hidden layers

import tensorflow as tf
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

def make_network(features,targets):
    np.random.seed(42)
    n_epochs = 64

    corrected_features_array = np.array(features)
    target_array = np.array(targets)

    scaler = preprocessing.StandardScaler()
    corrected_features_array = scaler.fit_transform(corrected_features_array)

    features_train, features_test, target_train, target_test = train_test_split(corrected_features_array,
                                                                               target_array,
                                                                               test_size=0.25,
                                                                               random_state=22)
    print('Fitting network...')
    

    network = tf.keras.Sequential()
    network.add(tf.keras.Input(shape=features_train.shape[1],))
    network.add(tf.keras.layers.Dense(units=32,
                            activation="relu",
                            kernel_regularizer=tf.keras.regularizers.l2(0.01)
                            )
               )

    network.add(tf.keras.layers.Dense(units=16,
                            activation="relu",
                            kernel_regularizer=tf.keras.regularizers.l2(0.01),))

    network.add(tf.keras.layers.Dense(units=1))

    network.compile(loss="mse",
                   optimizer="RMSprop",
                   metrics=["mse"])

    history = network.fit(features_train, target_train,
                         epochs=n_epochs,
                         verbose=0,
                         batch_size=100,
                         validation_data=(features_test, target_test))

    training_loss = history.history["loss"]
    test_loss = history.history["val_loss"]
    
#model report
    network.summary()


    epochs_count = range(1,len(training_loss)+1)

    plt.plot(epochs_count, training_loss,"k-")
    plt.plot(epochs_count, test_loss, 'r--')
    plt.legend(["training loss", "test loss"])
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.show()

    loss_diff = [element1 - element2 for (element1,element2) in zip(training_loss,test_loss)]

    plt.plot(epochs_count,loss_diff,'k-')
    plt.plot([0,n_epochs],[0,0],'c--')
    plt.ylim(-0.5,2)
    plt.xlabel("Epochs")
    plt.ylabel("Loss Difference")
    plt.show()

    predicted_target = network.predict(features_test)
    predicted_train = network.predict(features_train)


    fig, ax = plt.subplots()

    ax.plot(target_train, predicted_train,'b.')
    ax.plot(target_test, predicted_target,'r.')
    ax.plot([min(targets)-5,max(targets)+5],[min(targets)-5,max(targets)+5],color='gray', linestyle='dashed')

    # ax.set(xlim=(0,0.05), ylim=(0,0.05))
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.show()
    
    return network


#Create a target array for each performance metric to pass into the network
targets_active = [item[2] for item in targets]
targets_onset = [item[1] for item in targets]
targets_safe = [item[0] for item in targets]

#Run the network on your preferred target
trained_network = make_network(features, targets_active)
