<span style="color:white">
The Cost of a Mile - Trends in Car Devaluation
</span>  

Developed using Pandas, Numpy, Selenium, and Plotly libraries  
## by Josh Bartels [@Linkedin](https://www.linkedin.com/in/joshua-bartels-756309138/)

# Overview / Goals
- Extract: Build an API to extract real world car prices and mileage
- Transform: Clean the data to be ready for batch plotting and analysis
- Load: Store data in a central location that can easily be updated
- Analyze: Model the data to answer our guiding questions 

### **Questions:**  
> - How much should I spend to fix my old car?
> - How many miles should I expect to get per $ spent fixing my car?
> - When should I sell my car?
> - What cars retain their value best?

### **Situation:**  
This is how I see my car, shiny brand new with fine engineering and design:
 <p align="center">
  <img src="./images/Active_Dose_plot.png" width = 600>
 </p>
however, this is how everyone else sees my car, from 2010 with +200,000 miles and maybe a few dents:
 <p align="center">
  <img src="./images/Active_Dose_plot.png" width = 600>
 </p>
I drove every mile on this car and love it. I want to keep it as long as I can without making multiple particularly poor economic decisions.
This raises a real problem, I don't know how much it is *worth* to repair. The first thought is to compare the market price of the car to the cost of a fix, but this suggests it is rarely ever worth fixing.
The car still *has* to have value since it gets me from place to place (the role of a car). Instead of defining the value by the price of the car, lets define it as the number of miles.
So then our question becomes: How much is a mile worth on a Mazda3?
 
### **Approach**
> API 
    
### **Extracting Data:**  
To make an informed decision I need real data to compare costs.
 <p align="center">
  <img src="./images/Active_Dose_plot.png" width = 600>
 </p>
 
   With the inclusion of drug lifetime there is a dramatic difference in the safety and effectiveness.  The lowest molecular weight film (blue) delivers the drug too quickly and crosses our safety threshold, while the highest molecular weight (green) sits dangerously close to the minimum effective dose (MED).  Although close to the MED, we observe a desirable feature of an extended plateau in the case of the highest molecular weight modelled. <p>&nbsp;</p>  

# Part 2 : Interactive Dashboard [@render](https://delayed-drug-release-app.onrender.com) [@github](https://github.com/JMBartels/Delayed-Drug-Release/blob/main/Delayed-Drug-Release-App.py)
 
- The next goal is to design a membrane that has a plateau between MED and MSC and a duration around 15 days.
- Lets build an interactive simulation dashboard in Python with Plotly/Dash to explore designs intuitively with knobs that dynamically set our design variables.

 <p align="center">
  <!--<object data="filename.html" width="1600" height="3200"></object> -->
  <embed type="text/html" src="activeplot.html" width="600" height="700">
 </p>
  
- Follow the link to run the interactive web-deployed app on Render or use the github repo to run it on your machine.
[Link to Full Dash App Deployed on Render](https://delayed-drug-release-app.onrender.com){:target="_blank"}

 <p align="center">
  <img src="./images/example_plot2.png" style="width: 400px; border:1px solid #ddd;">
 </p>

<span style="color:red"> NOTE: the Render server is slow and will take a minute or two to load and 10-15 seconds to recalculate after you turn a knob, please be patient! </span> 
  <p>&nbsp;</p>


# Part 3 : Machine Learning [@github](https://github.com/JMBartels/Delayed-Drug-Release/blob/main/SimFilmNeuralNetwork.py)

<p align="center">
 <img src="./images/SimFIlm_actual_vs_pred_v2.png" width="600">
</p> 

- This system offers a complex relationship between the three input variables (MW, thickness, drug concentration) and the three performance metrics (is it safe, time to activate, active drug duration), and offers a rich platform for machine learning to model
- Simulate a database of membrane performance for 1,000 random possible designs
- Build a Neural Network with Tensorflow and scikit-learn trained on the simulated database
- Visualize the ability of the model to predict active drug duration  

Below is the function that takes the simulated database and builds/fits a neural network to predict active drug time from membrane design
```python 
def make_network(features,targets):
    np.random.seed(42)
    n_epochs = 64
    scaler = preprocessing.StandardScaler()
    corrected_features_array = scaler.fit_transform(corrected_features_array)

    features_train, features_test, target_train, target_test = train_test_split(corrected_features_array,
                                                                               target_array,
                                                                               test_size=0.25,
                                                                               random_state=22)
    network = tf.keras.Sequential()
    network.add(tf.keras.Input(shape=features_train.shape[1],))
    network.add(tf.keras.layers.Dense(units=32,
                            activation="relu",
                            kernel_regularizer=tf.keras.regularizers.l2(0.01)))

    network.add(tf.keras.layers.Dense(units=16, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01),))

    network.add(tf.keras.layers.Dense(units=1))

    network.compile(loss="mse",optimizer="RMSprop",metrics=["mse"])

    history = network.fit(features_train, target_train,epochs=n_epochs,verbose=0,
                         batch_size=100,
                         validation_data=(features_test, target_test))

    training_loss = history.history["loss"]
    test_loss = history.history["val_loss"]
```

<p align="center">
 <img src="./images/Loss_vs_epoch.png" width="600">
</p> 

- The model starts with very poor accuracy but improves significantly after 10 iterations (epochs) through the data
- This plot, at first glance, indicates sufficient fitting at 10 epochs, however the initial fits have such high loss that we cannot tell the fit quality beyond 10 epochs
- Lets look at the difference between the training loss and test loss to see if and when we get to high quality fits

 <p align="center">
 <img src="./images/LossDiff_vs_epoch-c.jpg" width="600">
</p> 

- Here we can see the model reaches our desired quality around 30 epochs and does not extend into the over-fitting regime 

# Wrap-up:
Overall, we were able to take basic chemistry principles and develop a model in python to explore drug release mediated by drug design.  We have an interactive dashboard available on the web that allows the user to key into their desired performance through intuitive exploration. Finally, we simulated a large number of membrane designs and trained a neural network to predict the performance metrics from membrane design. 

<p>&nbsp;</p>
<span style="color:gray;font-size=8px">
This project was conceived and coded solely by me (Josh Bartels), I hope you enjoyed it!
</span>  

