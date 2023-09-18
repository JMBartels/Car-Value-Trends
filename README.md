<span style="color:white">
Delayed Drug Release App
</span>  

## by Josh Bartels [@linkedin](https://www.linkedin.com/in/joshua-bartels-756309138/)

# Overview / Goals
- [X] Simulate and visualize drug release mediated through polymer dissolution. 
-	[X] Explore the nonlinear relationship between film design and active drug concentration. 
-	[X] Identify “just right” designs where active concentration is never too high for safety nor too low for effectiveness.
-	[X] Build machine learning architecture trained on simulated data to predict key membrane performance metrics
 
# Part 1 : Modelling the System
  <p align="center">
   <img src="./images/Film_Design.jpg" width = 500>
  </p>

**Problem**: In a delayed release system, there are competing effects governing the active drug concentration preventing it from being predicted simply.

**Goal**: Design a polymer coating that safely releases an active small molecule (drug) over a desired range of time. 
- Polymer film thickness decreases linearly with time: it dissolves at the same rate regardless of starting thickness.
- The length of the polymer chain (its molecular weight) has a non-linear effect on rate of polymer dissolution.  Longer polymer chains become more entangled, resulting in delayed dissolution. A great resource on this by Bae Soo Kong, Yong Sung Kwon, and Dukjoon Kim can be found at (Polymer Journal, Vol. 29, No. 9, pp 722-732 (1997); https://www.nature.com/articles/pj1997129.pdf).  I borrow a simplified dissolution rate vs molecular weight relationship and omit temperature effects for simplicity:
  <p align="center">
   <img src="./images/Rd_eqn.png" width = 200>  
  </p>
    Where Rd is the rate of dissolution, k is a rate constant we set to an arbitrary yet reasonable value, and Mw is the polymer molecular weight. The drug is not infinitely stable and either becomes inactive or eliminated from the body so that the active concentration will decay with a half-life:  
  <p align="center">
   <img src="./images/C_eqn.png" width = 200>  
  </p>
    Where C is the current concentration, C0 is the initial concentration, dt is the time passed, and t1/2 is the half-life.  Notice that a higher drug concentrations will result in a sharper decay in active concentration. There are two competing effects, linear drug introduction and non-linear deactivation/removal.  Since the drug is continually introduced through film dissolution, there is no constant rate of decay and we must continually recalculate the decay rate with the current concentration.
- Initial plots of active drug concentration vs. time for three different molecular weights and a constant thickness:
 <p align="center">
  <img src="./images/Active_Dose_plot.png" width = 500>
 </p>
    With the inclusion of drug lifetime there is a dramatic difference in the safety and effectiveness of these three film designs.  The lowest molecular weight film (blue) delivers the drug too quickly and crosses our safety threshold, while the highest molecular weight (green) sits dangerously close to the minimum effective dose (MED).  Although close to the MED, we observe a desirable feature of an extended plateau in the case of the highest molecular weight modelled. <p>&nbsp;</p>  

# Part 2 : Interactive Dashboard [@render](https://delayed-drug-release-app.onrender.com) [@github](https://github.com/JMBartels/Delayed-Drug-Release/blob/main/Delayed-Drug-Release-App.py)

 <p align="center">
  <img src="./images/example_plot2.png" style="width: 500px;">
 </p>  
 
- The next goal is to design a membrane that has a plateau between MED and MSC and a duration around 15 days.
- Guess-and-check is far too slow for this so instead we build an interactive plot in Python with Plotly/Dash to explore designs intuitively with knobs that dynamically set our membrane design variables.
- Follow the link to run the web-deployed app on Render or use the github repo to run it on your machine.
<span style="color:red">
- NOTE: the Render server is slow and will take a minute to load and 10-15 seconds to recalculate after you turn a knob, please be patient!
</span>  
  <p>&nbsp;</p>


# Part 3 : Machine Learning

 <img src="./images/SimFIlm_actual_vs_pred.png" width="500">
 
- This system offers a complex relationship between the input variables (MW, thickness, drug concentration) and the performance metrics (is it safe, time to activate, active drug duration), and offers a rich platform for machine learning to analyze
- Simulate a database of membrane performance
- Build a neural network with Tensorflow and scikit-learn and train on the database
- Visualize the ability of the model to predict active drug duration 
