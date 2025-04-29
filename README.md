<span style="color:white">
The Cost of a Mile - Trends in Car Devaluation
</span>  

Developed using Pandas, Numpy, Selenium, and Plotly libraries  
No AI tools were used in the development and coding of this project  
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
  <img src="./images/car_isolder.jpg" width = 600>
 </p>

However, this is how everyone else sees my car, from 2010 with +200,000 miles and maybe a few dents:

 <p align="center">
  <img src="./images/car_isolder.jpg" width = 600>
 </p>

I drove every mile on this car and love it. I want to keep it as long as I can without making multiple particularly poor economic decisions.
This raises a real problem, I don't know how much it is *worth* to repair. The first thought is to compare the market price of the car to the cost of a fix, but this suggests it is rarely ever worth fixing.
The car still *has* to have value since it gets me from place to place (the role of a car). Instead of defining the value by the price of the car, lets define it as the number of miles.
So then our question becomes: How much is a mile worth on a Mazda3?
 
### **Approach**
> Build and API to search and retrieve data from Autotrader
    
# **Extracting Data:**  
To make an informed decision I need real data to compare costs. We will scrape information from Autotrader in the Boston area using Selenium in Python to control Chrome:

 <p align="center">
  <img src="./images/Mazda3Listings.PNG" width = 500>
 </p>
 
   There are a few key parts of this code: 
   1. Understanding the syntax for an Autotrader URL --> how to execute a search
   1. Get the page to load in all the data using page navigation (get around "infinite scrolling")
   1. Get component information from each listing (Price, Miles, Listing Name)

```python
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

## Input your search parameters here ##
criteria = {"postcode": "02138",
    "radius": "100",
    "year_from": "2008",
    "year_to": "2023",
    "price_from": "1000",
    "price_to": "40000"}

cars = [{"make": "Mazda","model": "Mazda3"}]

## Build the search url using Autotrader's  convention ##
url = "https://www.autotrader.com/cars-for-sale/all-cars/" + \
    f"{car['make']}/" + \
    f"{car['model']}?" + \
    f"searchRadius={criteria['radius']}&" + \
    f"startYear={criteria['year_from']}&" + \
    f"endYear={criteria['year_to']}&" + \
    f"numRecords=100&" +\
    f"zip={criteria['postcode']}"

driver.get(url)
print(f"Searching for {car['make']} {car['model']}...")
time.sleep(5) 

source = driver.page_source
    
## Scroll down fractions of the web page to let the autoscroll info load in with 4.8s loading times##
waitlist = [0.2,0.4,0.6,0.8,0.95]
for num in waitlist:
     driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight*{num});")
     time.sleep(4.8)
    
## With the web page now loaded, find each element, identified by inspecting the webpage html
prices = driver.find_elements(By.XPATH, '//div[@data-cmp="firstPrice"]')
miles = driver.find_elements(By.XPATH, '//div[@data-cmp="mileageSpecification"]')
fullname = driver.find_elements(By.XPATH, '//h2[@aria-level="3"]')

## Extract the text of each element into a list
price_list = []
for p in range(len(prices)):
    price_list.append(prices[p].text)

miles_list = []
for m in range(len(miles)):
    miles_list.append(miles[m].text)
    
fullname_list = []
for n in range(len(fullname)):
    fullname_list.append(fullname[n].text)
```

   <p>&nbsp;</p>  

 <p align="center">
  <embed type="text/html" src="RawCarsData.html" width="800" height="800">
 </p>

# **Transform/Clean Data:**
 
- The next goal is to design a membrane that has a plateau between MED and MSC and a duration around 15 days.
- Lets build an interactive simulation dashboard in Python with Plotly/Dash to explore designs intuitively with knobs that dynamically set our design variables.

 <p align="center">
  <!--<object data="filename.html" width="1600" height="3200"></object> -->
  <embed type="text/html" src="Milestogo.html" width="800" height="800">
 </p>
  
- Follow the link to run the interactive web-deployed app on Render or use the github repo to run it on your machine.
[Link to Full Dash App Deployed on Render](https://delayed-drug-release-app.onrender.com){:target="_blank"}

 <p align="center">
  <img src="./images/example_plot2.png" style="width: 400px; border:1px solid #ddd;">
 </p>

<span style="color:red"> NOTE: the Render server is slow and will take a minute or two to load and 10-15 seconds to recalculate after you turn a knob, please be patient! </span> 
  <p>&nbsp;</p>
  

# Wrap-up:
We obtained a real-world answer to our question: if I spend $2700 fixing my car I should get 21,000 miles before my next major fix, otherwise it is cheaper to be driving a different car.

<p>&nbsp;</p>
<span style="color:gray;font-size=8px">
This project was conceived and coded solely by me (Josh Bartels), I hope you enjoyed it!
</span>  

