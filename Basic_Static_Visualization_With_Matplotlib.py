# Basic static visualization with matplotlib (McKinney Ch 9)
# https://learning.oreilly.com/library/view/python-for-data/9781491957653/ch09.html#vis
# 
# - For creating static graphics for print or web, it is easier and quicker to use matplotlib and add-on libraries like pandas and seaborn. 
#     - matplotlib
#     - pandas
#     - seaborn
# 
# 
# - For other data visualization requirements such as interactive web-based visualizations, among several alternatives it may be useful to learn 
#     - Bokeh and/or 
#     - Plotly

# To display the output of plotting commands inline within frontends like the Jupyter notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# To add some basic interaction such as pan and zoom to the matplotlib charts
get_ipython().run_line_magic('matplotlib', 'notebook')

# importing all the needed libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn


# A Note of caution: One nuance of using Jupyter notebooks is that plots are reset after each cell is evaluated, so for more complex plots you must put all of the plotting commands in a single notebook cell.

# Two approaches to create charts in matplotlib
# 
# - 1) The shortcut option to quickly create a plot uses .plot() method.
# - 2) The better route is a two-step process that requires 
#     - 1) creating a figure oject and 
#     - 2) creating subplots. 

# A Figure object is the outermost container for a matplotlib graphic, which can contain multiple Axes objects. One source of confusion is the name: an Axes actually translates into what we think of as an individual plot or graph (rather than the plural of “axis,” as we might expect).
# 
# You can think of the Figure object as a box-like container holding one or more Axes (actual plots). Below the Axes in the hierarchy are smaller objects such as tick marks, individual lines, legends, and text boxes. Almost every “element” of a chart is its own manipulable Python object, all the way down to the ticks and labels:
# ![image.png](attachment:image.png)
# 
# Source: https://realpython.com/python-matplotlib-guide/

# #### Create a:
# - line plot
# - histogram
# - scatter plot
# - bar plot
# - pie chart

# ### Creating a line plot

# Creating a simple line plot using .plot() method. 	Plot y versus x as lines and/or markers.
# plt.clf()                                                #--- to clear the plotting space 
plt.figure(figsize=(9,7))                                 #--- You need to set the figure size before you plot.
plt.plot(np.random.randn(10), np.random.randn(10),         # x and y values generated randomly
         color='purple', linestyle='dashed', linewidth=2,  # Specifying line properties (optional)
         marker='x', markersize=8)                         # Specifying marker properties (optional)


# #### A note of caution: When you use a plotting command like plt.xxxxx(), matplotlib draws on the last figure and subplot used
# 
# so for example if you do >>>  
# plt.plot([3,4,1,2,8,6,7,8,9,10]) and redraw the original s1 plt.plot(s1)
# or plt.subplots_adjust()

# Let's plot another line with following values for Y
plt.plot([3,4,1,2,8,6,7,8,9,10], 'g--')


# ### Creating a bar chart
# - Method to use are .bar() and.barh()
# - For detailed parameter list see: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html

plt.barh(['Sweden','ROC','Netherlands'],[3,7,5], height =.5)
plt.title('Winter Olympics Total Medal Count')


# #### Since we used plt.plot() method, all the plots are being created in the default plot container above 

# ### Creating an histogram
# 
# - Method to use .hist()
# - For detailed paramater list see: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.hist.html#matplotlib.pyplot.hist

plt.hist(np.random.random(50), bins=10, color='blue')
# Since we used plt.plot() method, all the plots are being created in the same plot container above


# ### Creating a scatter plot
# - Method to use .scatter()
# - For detailed paramater list see: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.scatter.html#matplotlib.pyplot.scatter


plt.scatter([3,4,1,2,8,6,7,8,9,10], [3,4,1,2,8,6,7,8,9,10], color='red')
# Since we used .plot() method, all the plots are being created in the same plot container above


# ### Creating a pie chart
# - Method to use is .pie()
# - For detailed paramater list see: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html


# Use .clf() to clear the plot area
plt.clf()

# Create pie chart
plt.pie([3,7,5,4],labels=['Sweden','ROC','Netherlands','China'], autopct='%.2f')


# ## A better route... creating a named figure container and subplots within it
# - add_subplot(1,1,1) --> Creating a figure with just one subplot has the same visual effect of creating one and avoids the problems above.
#     - myPlot = plt.figure().add_subplot(1,1,1)
# 
# 
# - subplots(rows, columns) --> Creating a figure with a grid of subplots. This creates a new figure and returns a NumPy array containing the created subplot objects
#     - fig, inPlots = plt.subplots(rows, columns)
#     
#     
# - By no means these are the only two methods to create multiple subplots. See https://towardsdatascience.com/the-many-ways-to-call-axes-in-matplotlib-2667a7b06e06
# 
# 

# Create a figure object -- better way to create a named container unlike .plot()
myFig = plt.figure(figsize=(7, 5))

# Create subplots using add_subplot() method and following will create 1x1 grid
myPlot = myFig.add_subplot(2,2,2)
myPlot.bar(['Apple', 'Banana','Cherry','Dragon fruit'], [10,8,5 ,12], width=0.5)

# Create the figure object -- better way to create a named container unlike .plot()
myFig2 = plt.figure(figsize=(9,9))

# Add a plot in the 2nd position
myPlot1 = myFig2.add_subplot(2,2,2)
myPlot1.scatter([4,1,9,5], [10,8,5,12], color='blue')

# Add a plot in the 3rd position
myPlot2 = myFig2.add_subplot(2,2,3)
myPlot2.scatter([4,1,9,5], [10,8,5,12], color='red')

# Now the 3rd plot
myPlot3 = myFig2.add_subplot(2,2,1)
myPlot3.bar(['apple','banana'], [5,9], width=.5)

# Create a figure object -- better way to create a named container unlike .plot()
myFig1 = plt.figure(figsize=(10, 7))

myFig1.suptitle("This is the super title")

# Create subplots using add_subplot() method. Following will create a 2x2 grid of subplots. 
# the last parameter refers to subplot number
myPlot1 = myFig1.add_subplot(2,2,1)
myPlot2 = myFig1.add_subplot(2,2,2)
myPlot3 = myFig1.add_subplot(2,2,3)
myPlot4 = myFig1.add_subplot(2,2,4)

# Add a scatter plot in first position with two different colored markers
myPlot1.scatter([1,2,3], [6,7,8], color='blue', label='Blue')
myPlot1.scatter([6,7,8], [1,4,8], color='green', label='Grn')
myPlot1.set_title("Scatter colors")
myPlot1.legend(loc='best')


# Add line chart in the 2nd position
myPlot2.plot([4,1,3,6,3,7,9,2], 'k.', label="Dots")
myPlot2.plot([4,1,3,6,3,7,9,2], 'k--', label="Dashes")
myPlot2.set_title("Line Styles")
myPlot2.legend(loc='best')


# Ass plots in the 3rd and 4th position
myPlot3.pie([6,1,8,2], labels=['MSIS','MBA','MSBA','MSQMM'])
myPlot4.bar(['MSIS','MBA','MSBA','MSQMM'],[6,1,8,2], width=0.5)
myPlot3.set_title("Pie")
myPlot4.set_title("Bar")


# You do not need to specify plots in each of the subplot area...
myPlot5 = plt.figure(figsize=(10,6)).add_subplot(2,3,3)

