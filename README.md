<span style="color:red">
Drug Release App
</span>


## by [Josh Bartels](https://www.linkedin.com/in/joshua-bartels-756309138/)

# Overview / Goals

- [X]	Simulate and visualize drug release mediated through polymer dissolution. 
-	[X] Explore the nonlinear relationship between film design and active drug concentration. 
-	[X] Identify “just right” designs where active concentration is never too high for safety nor too low for effectiveness.
-	[X] Build machine learning architecture trained on simulated data to predict key membrane performance metrics
 
# Part 1 : Modelling the System

<img src="./images/Film_Design.jpg" width = 500>

- The problem and design
- Science of it: equations and explanation
- Initial plots of active drug concentration


# [Part 2 : Interactive Dashboard](https://delayed-drug-release-app.onrender.com)

<img src="./images/example_plot2.png" style="width: 500px;">

- Interactive data visualization using Plotly Dash
- Try making a membrane that is "just right"


# Part 3 : Machine Learning

 <img src="./images/SimFIlm_actual_vs_pred.png" width="500">
 
- Simulate a database of membrane performance (if it is safe, time to activate, and duration of drug activity) 
- Build and train a Neural Network on the database
- Visualize model quality
