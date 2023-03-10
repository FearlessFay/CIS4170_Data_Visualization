#!/usr/bin/env python
# coding: utf-8

# # Putting together plots created in different visualization libraries using Panel 

# ### Note: The material covered for the Panel library requires a good grasp of the following python topics:
# - function and function definition
# - parameters and arguments
# - keyword and positional arguments
# - return statement
# 
# Additional helpful topics
# - design patterns such as decorators. Read more on this https://www.datacamp.com/community/tutorials/decorators-python

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'notebook')


# In[2]:


# importing libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn

# Import any plotting library that you plan to use
...


# In[3]:


# Now import panel with an alias pn
import ... as pn

#import widgets
...

# In the classic Jupyter notebook environment, first make sure to load the pn.extension(). 
# Panel objects will then render themselves if they are the last item in a notebook cell.
pn...()


# In[4]:


# Next 3-4 lines in case bokehJS does not load. This will also ensure plotting is done inline


# In[5]:


# Read the dataset.. This is a slightly updated dataset with two new columns of Origin_Country and Weight_Size
auto = pd...("AutoMPG.xlsx")

auto


# ### Code Without Panel function and decorator

# In[6]:


# The typical code for matplotlib scatterplot with markers colored and sized based on certain columns in your dataframe

# cleaning out the subplot space
myFig = plt.figure()
myPlot = ...

# Color coding based on values in a specific column in matplotlib requires that we plot markers in each value group separately.
# Hence the auto.groupby() statement to creates groups based on countries as we are using that column to color the markers
for country, df in auto.groupby('Origin_Country'):       
    
    # Note here we are using matplotlib's scatter method rather than using the pandas's plot method
    myPlot.scatter(x=..., y=..., # x and Y axis columns
                   s=(df['Weight']/200)**2, edgecolor=..., #marker size and marker edge color
                   label=...) # legend entry

# adding the legend box 
myPlot.legend()

# Rendering the figure --> This line of the code was missing in the video 
myFig


# In[7]:


# We will use reactive programming API for gathering our plots from differnt libraries
# First explicity declare the widget elements for various parameters that our plotting function uses

# Select dropdown widgets each for x and y axis variable selection
uX = pn.widgets.Select(...)
uY = pn.widgets.Select(...)


# ### Same code as above wrapped up in function with the .depends decorator: Scatter plot with matplotlib

# In[35]:


# Function declaration with pn.depends decorator to link widgets to the function. 

def mpl_Scatter(uXVar, uYVar):
    
    # Create the figure container and subplot
   ...
    
    # Removing the padding space from around the subplot
    rFig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
      
    # For loop to render the markers separately for each country
    for country, df in auto.groupby('Origin_Country'):            
        
        # Note here we are using matplotlib's scatter method rather than using the pandas's plot method
        rPlot.scatter(...                                 # X and Y axis variables per user selection
                      s=(df['Weight']/300)**2, edgecolor='white', alpha=0.75, #sizing the markers based on Weight column
                      label=country)                                        # adding the label
    
    # adding the legend box    
    rPlot.legend()
    
    # Setting the proper labels for x and y axes
    rPlot.set_xlabel(...)
    rPlot.set_ylabel(...)
    
    # return the figure container so that it can be used by the API functions
    return rFig


# In[29]:


### Create the scatter plot using plotly, first without panel function and decorator


# In[30]:


pxFig = px.scatter(... # x and y
                   ... # color and size
                  width=400, height=300) #height and width

pxFig.show()


# In[64]:


...
def plotly_Scatter(uxVar, uYVar):
    # Create the scatter object
    pxFig = px.scatter(... # x and y
                       ... # color and sizeauto, x=uxVar, y=uYVar, 
                       color_discrete_sequence=["green","orange", "blue"],
                       width=550, height=400)
    
    # Update the margin space around and adjust location of legend box
    pxFig.update_layout(margin=dict(l=20, r=20, t=0, b=0),
                       legend_x=0, legend_y=1)
    
    # Turn off x and y gridlines
    pxFig.update_xaxes(showgrid=False)
    pxFig.update_yaxes...
    
    # Always return the object back
    return ...


# ### Putting together these plots now using GridSpec instead of pn.Row and pn.Column alone to make it easier to organize
#  https://panel.holoviz.org/reference/layouts/GridSpec.html

# In[65]:


# create a gridspec 
autoGS = pn.GridSpec(sizing_mode='stretch_both', width=800, height=500)

# Specify what each row and column will contain

# The top row will have both the widgets
autoGS[0, 0] = pn.Column(... margin=0)

# This will create two columns [1,0] and [1,1] in the 2nd row each column occupying plot from a different library
autoGS[1,0] = pn.Column(..., margin=0, align="center")
autoGS[1,1] = pn.Column(..., margin=0, align="center")

# Launch the viz as an app in a separate browser window with .show()
autoGS.show()

