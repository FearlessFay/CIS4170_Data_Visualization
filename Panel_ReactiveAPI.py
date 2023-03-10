#!/usr/bin/env python
# coding: utf-8

# ### Note: The material covered for the Panel library requires a good grasp of the following python topics:
# - function and function definition
# - parameters and arguments
# - keyword and positional arguments
# - return statement
# 
# Additional helpful topics
# - design patterns such as decorators. Read more on this https://www.datacamp.com/community/tutorials/decorators-python

# # Interact and Reactive API
# 
# - The types of widgets available in Panel library is vast. You can find complete list here: https://panel.holoviz.org/user_guide/Widgets.html
# 
# 
# # Reactive programming API
# 
# - Very similar to the interact function but makes it possible to explicitly declare the inputs to the function using the **@depends** decorator.
# 
# 
# -  By decorating a function with pn.depends, we declare that when we change these parameters the function should be called with their new values.
# 
# 
# - This approach makes it explicit which parameters the function depends on and ties the function directly to the objects that control it. 
# 
# 
# - Makes the layout of the different components more explicit.


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'notebook')

# first import our usual libraries
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# Now import panel with an alias pn
import panel as pn

from panel.interact import interact, interactive, fixed, interact_manual
from panel import widgets

# In the classic Jupyter notebook environment, first make sure to load the pn.extension(). 
# Panel objects will then render themselves if they are the last item in a notebook cell.
pn.extension()


# Read the dataset
auto = pd.read_excel("AutoMPG.xlsx")

auto


# The typical 3-line code for matplotlib scatterplot

# Create the figure container object
myFig = plt.figure(figsize=(10,7))

# Now create a subplot
myPlot = myFig.add_subplot(1,1,1)

# Using pandas plot method and ax attribute create a scatter plot of Wt X HP
auto.plot.scatter('Weight', 'Horsepower', color='blue', s=10**2, alpha=0.1, ax=myPlot)

# Let's explore what columns exists in our dataset
auto.columns 


# First explicity declare the widget elements for various parameters that our plotting function uses

# Select dropdown widgets each for x and y axis variable selection
uX = pn.widgets.Select(name='X axis variable selection', 
                       options=['Cylinder', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MPG'], 
                       value='MPG')

uY = pn.widgets.Select(name='Y axis variable selection', 
                       options=['Cylinder', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MPG'], 
                       value='Displacement')

# Color picker widget
uC = pn.widgets.ColorPicker(name='C', value='#654321')

# IntSlider widget for size
uS = pn.widgets.IntSlider(name='S', start=1, end=20, value=5)

# Function declaration with pn.depends decorator to link widgets to the function. 

@pn.depends(uX, uY, uC, uS)
def react_mpl_plot(uXVar, uYVar, uColor, uSize):
    
    # Create the figure container and subplot
    rFig = plt.figure(figsize=(7, 5))
    rPlot = rFig.add_subplot()
    
    # Manipulate the marker size variable to allow for proper marker size
    uSize=uSize**2
    
    # Call the .scatter() method with specs for x,y, color, size, and alpha i.e. transparency value for marker 
    auto.plot.scatter(uXVar, uYVar, ax=rPlot, color=uColor, s=uSize, alpha=0.25)
    
    # return the figure container so that it can be used by the API functions
    return rFig
   
from bokeh.resources import INLINE
import bokeh.io
bokeh.io.output_notebook(INLINE) 

# finally lay out the widgets and the react_mpl_plot function explicitly.

# Use servable method to run the app within the notebook (rendering is somewhat unpredictable)
#pn.Row(pn.Column(uX,uY,uC,uS),react_mpl_plot).servable()

# For more realiable rendering of the app use .show() method that launches the viz in a new browser window
pn.Row(pn.Column(uX,uY,uC,uS),react_mpl_plot).show("This is the interactive panel viz for visualizing automobile features")


# ## Now let's create a plot that allows to use one of the variables to determine the size of the individual markers rather than letting the viewer control the size of markers

# #### In this example, we will size the marks by variable "Weight", rest of the function code otherwise remains unchanged

# First declare the widget elements for various parameters that our plotting function uses -- as before

# Select dropdown widgets each for x and y axis variable selection
uX = pn.widgets.Select(name='X', options=['Cylinder', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MPG'], value='Horsepower')
uY = pn.widgets.Select(name='Y', options=['Cylinder', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MPG'], value='Acceleration')

# Color picker widget
uC = pn.widgets.ColorPicker(name='C', value='#654321')

# Notice in this case we are not declaring the size widget as we had in the previous case


# Function declaration with pn.depends decorator to link widgets to the function -- changes to the marker size option

# Notice again that the decorator and function specs are missing the user defined parameter for size uS
@pn.depends(uX, uY, uC)
def react_mpl_plot_weight(uXVar, uYVar, uColor):
    
    # Create the figure container and subplot
    rFig = plt.figure(figsize=(8.5,7))
    rPlot = rFig.add_subplot()
    
    # Manipulate the marker size variable based on the weight of the vehicle
    uSize=((auto.Weight)/200)**2
    
    # Call the .scatter() method with specs for x,y, color, size, and alpha i.e. transparency value for marker 
    auto.plot.scatter(uXVar, uYVar, ax=rPlot, color=uColor, s=uSize, alpha=0.25)
    
    # return the figure container so that it can be used by the API functions
    return rFig
  
  
# finally lay out the widgets and the react_mpl_plot_weight function explicitly.
# pn.Row(pn.Column(uX,uY,uC), react_mpl_plot_weight).servable()
pn.Row(pn.Column(uX,uY,uC), react_mpl_plot_weight).show("Using markers sized by car weight")


# # Practice exercise tasks
# 
# - In the above example, can you modify the code and add a CheckButtonGroup widget that allows the users to filter out cars by the country of origin? [CheckBoxWidget has implementation issues and does not work.]
# 
# - See all the widget possibilities here: https://panel.holoviz.org/user_guide/Widgets.html

# ### Steps to get you started.... 


# What are the values in the origin column?
sorted(auto.Origin.unique()) 


# ### how do we write the code for CheckButtonGroup widget?
# 
# checkbutton_group = pn.widgets.CheckButtonGroup(name='Check Button Group', 
#                                             value=['Apple', 'Pear'], 
#                                             options=['Apple', 'Banana', 'Pear', 'Strawberry'])
# 
# checkbutton_group

uCntry = pn.widgets.CheckButtonGroup(name="Auto Country of Origin",
                                  value=[1], # Values already pre-selected
                                  options=[1,2,3]) # All the possible values
uCntry



### Prepare the dataset to show only countries selected in the check box
## Hint: Use .isin()



# Now write the code for the function -- 
# start with @pn.depends(nameOfYourWidgetVariable) followed by def functionName on the next line  

@pn.depends ....

# Now layout all the widgets and function calls using .show() or .servable() methods
