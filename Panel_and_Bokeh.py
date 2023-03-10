#!/usr/bin/env python
# coding: utf-8

# # Adding bokeh plots to Panel based visualizations

get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'notebook')

# importing libraries
import matplotlib.pyplot as plt
import pandas as pd

# You will likely need to import any library that you plan to use, just to be safe
import pandas_bokeh


# Loading bokeh inline
from bokeh.resources import INLINE
import bokeh.io
bokeh.io.output_notebook(INLINE) 


# Now import panel with an alias pn
import panel as pn

# In the classic Jupyter notebook environment, first make sure to load the pn.extension(). 
# Panel objects will then render themselves if they are the last item in a notebook cell.
pn.extension()


# Read the dataset.. This is a slightly updated dataset with two new columns of Origin_Country and Weight_Size
# Always use relative file path. Avoid using absolute filepath.
# More on difference between absolute and relative file paths: https://www.educative.io/edpresso/absolute-vs-relative-path 

auto = pd.read_excel("AutoMPG.xlsx")

auto


# # Declare the widgets explicitly
# - Since we will be using Panel's reactive programming API.

# We will use reactive programming API for agthering our plots from differnt libraries
# First explicity declare the widget elements for various parameters that our plotting function uses

# Select dropdown widgets each for x and y axis variable selection
uX = pn.widgets.Select(name='X-Axis Variable Selection', 
                       options=['Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MPG'], 
                       value='Horsepower', width=175)

uY = pn.widgets.Select(name='Y-Axis Variable Selection', 
                       options=['Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MPG'], 
                       value='Acceleration', width=175)

uY2 = pn.widgets.Select(name='Y2-Axis Variable Selection', 
                       options=['Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MPG'], 
                       value='Displacement', width=175)


# # Creating plots with bokeh
# 
# - Since Panel library is built on Bokeh internally, the Bokeh model is simply inserted into the plot with Bokeh **pane**. The Bokeh pane allows displaying any displayable Bokeh model inside a Panel app. This pane type is very useful for combining raw Bokeh code with the higher-level Panel API.  

# ## A few things to know about bokeh - I:
# - Bokeh provides several APIs from which you will need import objects as needed. List of APIs include .plotting, .models, .io, .layouts, .palettes, and .settings. You can read more about them here: https://docs.bokeh.org/en/latest/docs/reference.html
# 
# 
# - While bokeh can work directly with pandas dataframe objects, it has its own native data structure called [**ColumnDataSource**](https://docs.bokeh.org/en/latest/docs/user_guide/data.html) that you will need to use if you want to use certain interactive features such as linked brushing.
# 
# 
# - As the name suggests, it organizes data by columns making them more efficient for rendering. You can create a CDS using either a dictionary or directly from a pandas DataFrame or GroupBy object
# 
# 
# - Important Note: **All columns in a ColumnDataSource have the same length i.e. same number of elements**. Therefore, all sequences of values that you pass to a single ColumnDataSource must have the same length as well. If you try to pass sequences of different lengths, Bokeh will not be able to create your ColumnDataSource.


# Set of import statements needed for bokeh
# you need to import the modules as needed from various bokeh interfaces such as .plotting, .layouts, etc. 
# using following syntax

# import figure and gridplot objects
from bokeh.plotting import figure
from bokeh.layouts import gridplot

# ColumnDataSource is bokeh's native data structure similar to pandas dataframe. 
from bokeh.models import ColumnDataSource

# To change the color and shape of the markers
from bokeh.transform import factor_cmap, factor_mark


# A simple example of creating ColumnDataSource - from a dictionary

myData = {'x_values': [1, 2, 3, 4, 5],
          'y_values': [6, 7, 2, 3, 6]}

myDF = pd.DataFrame(myData)
myCDS = ColumnDataSource(data=myData)

print(myDF)
print(myCDS.data)

#To add a new **column** to an existing ColumnDataSource:

new_sequence = [8, 1, 4, 7, 3]
myCDS.data["z_val"] = new_sequence
print(myCDS.data)


# # Creating a ColumnDataSource from a dataframe
# If you use a pandas DataFrame, the resulting ColumnDataSource in Bokeh will have columns that correspond to the columns of the DataFrame. The naming of the columns follows these rules:
# 
# - If the DataFrame has a named index column, the ColumnDataSource will also have a column with this name.
# 
# - If the index name is None, the ColumnDataSource will have a generic name: either index (if that name is available) or level_0.
# 
# - See more on CDS here: https://docs.bokeh.org/en/latest/docs/user_guide/data.html#providing-data-as-a-columndatasource

# Creating a CDS from auto dataframe

autoCDS = ColumnDataSource(auto)
autoCDS.data


# ## A few more things to know about bokeh - II:
# - [Different interactive tool options](https://docs.bokeh.org/en/latest/docs/user_guide/tools.html)
# - [Detailed guide on styling with visual attributes](https://docs.bokeh.org/en/latest/docs/user_guide/styling.html)
# - [Changing colors and marker types based on categorical columns](https://docs.bokeh.org/en/latest/docs/user_guide/data.html#mapping-marker-types)

@pn.depends(uX, uY, uY2)
def bokeh_plot(uXVar, uYVar, uYVar2):
    
    # specify which tools you want to enable. If not specified default setting will be used when charts are rendered
    TOOLS = "box_select,lasso_select,help, pan"

    # create a new figure container 
    left = figure(tools=TOOLS, plot_width=450, plot_height=320, x_axis_label= uXVar, y_axis_label= uYVar, title="Scatter-1")
    
    # Now add a circle renderer
    left.circle(uXVar, uYVar, alpha=.6,  
                
                # Setting the size of markers based on weight of the vehicle
                size='Weight_Size',             
                
                # coloring markers based on the country of origin
                color=factor_cmap('Origin_Country', 'Category10_3', list(auto['Origin_Country'].unique())),
 
                # Adding the legend based on the country of origin
                legend_field="Origin_Country", 
                
                # Setting behavior for what happens when glyphs are selected/not selected.
                nonselection_fill_alpha=0.2, nonselection_fill_color="gray", 
                nonselection_line_color="gray", nonselection_line_alpha=0.2,
                
                # Setting the data source to autoCDS. This will also automatically allow for linked brushing
                source=autoCDS)
    
    # Starting the x- and y-range at 0 
    left.y_range.start = 0
    left.x_range.start = 0
    
    # reducing clutter by removing gridlines
    left.grid.grid_line_color = None
    
    # Making the axis and tick properties somewhat mute
    left.axis.axis_line_color = "gray"
    left.axis.axis_line_width = 1
    
    left.axis.minor_tick_line_color = None
    left.axis.major_tick_out = 3
    left.axis.major_tick_in = 0
    left.axis.major_tick_line_width = 1
    left.axis.major_tick_line_color = "gray"

    # adjusting legend properties
    left.legend.label_text_font_size = "9px"
    left.legend.glyph_width = 10
    left.legend.spacing = 1
    left.legend.padding = 1
    left.legend.margin = 2    
    
    # create the second scatter plot with a square renderer
    right = figure(tools=TOOLS, plot_width=450, plot_height=320, x_axis_label= uXVar, y_axis_label= uYVar2, title="Scatter-2")
    
                   # Linking of x and y ranges to allow for linked panning.
                   # ADVISABLE TO use only when both plots have similar limits on the ranges
                   # x_range=left.x_range, y_range=left.y_range)
    
    right.square(uXVar, uYVar2, size='Weight_Size', 
                 #alpha=.3, legend_field="Origin_Country", color=factor_cmap('Origin_Country', 'Category10_3', list(auto['Origin_Country'].unique())),
                 #nonselection_fill_alpha=0.2, nonselection_fill_color="gray",nonselection_line_color="gray", nonselection_line_alpha=0.2,
                 source=autoCDS)
 
    # putting them in grid
    bkPlot = gridplot([[left, right]])
    
    # Wrapping the bokeh gridplot in Panel's .Bokeh pane. 
    bokeh_pane = pn.pane.Bokeh(bkPlot)
    
    # returning bokeh pane object
    return bokeh_pane


# # Create the scatter plot using matplotlib


# Function declaration with pn.depends decorator to link widgets to the function. 
@pn.depends(uX, uY)
def react_mpl_plot_weight(uXVar, uYVar):
    
    # Create the figure container and subplot
    rFig = plt.Figure(figsize=(6,5))
    rPlot = rFig.add_subplot()
    
    # Removing the padding space from around the subplot
    rFig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
      
    # For loop to render the markers separately for each country
    for country, df in auto.groupby('Origin_Country'):            
        
        # Note here we are using matplotlib's scatter method rather than using the pandas's plot method
        rPlot.scatter(df[uXVar], df[uYVar],                                 # X and Y axis variables per user selection
                      s=(df['Weight']/300)**2, edgecolor='gray', alpha=0.5, #sizing the markers based on Weight column
                      label=country)                                        # adding the label
    
    # adding the legend box    
    rPlot.legend()
    
    # Setting the proper labels for x and y axes
    rPlot.set_xlabel(uXVar)
    rPlot.set_ylabel(uYVar)
    
    #setting y axis starting points to 0
    rPlot.set_ylim(bottom=0)
    
    # return the figure container so that it can be used by the API functions
    return rFig


# # Create the scatter plot using pandasBokeh

# Function declaration with pn.depends decorator to link widgets to the function. 
@pn.depends(uX, uY)
def react_pandasBokeh_plot_weight(uXVar, uYVar):
    
    # Since bokeh uses only the columns inside the dataframe, 
    # we need to create a column to use for sizing the markers based on weight
    auto['wt_size']=auto.Weight/300 
    
    # instead of specifying backend attribute, you can also directly call plot_bokeh method as below
    bkPlot = auto.plot_bokeh.scatter(uXVar, uYVar, 
                                     figsize=(450,320),
                                     category='Origin_Country', colormap='Viridis', 
                                     line_color='gray', line_width=1,
                                     fontsize_legend=8, legend="top_left",                                      
                                     size='wt_size', alpha=.5)
    
    # For detailed list of visual styling elements that you can customize in the underlying bokeh library, 
    # see https://docs.bokeh.org/en/latest/docs/user_guide/styling.html
    bkPlot.y_range.start = 0
    bkPlot.grid.grid_line_color = None
    bkPlot.axis.minor_tick_line_color = None
    bkPlot.legend.padding = 1
    bkPlot.legend.spacing = 1
 
    return bkPlot


# ### Putting together these plots together with pn.Tabs, pn.Row, and pn.Column


# Let's add a title and organize the widgets 
title = pn.Row("** Auto MPG Explorer **",  margin=20, background='#f0f0f0')
xyWid = pn.Row(uX, uY, uY2, margin=20, background='#f0f0f0')


tab1 = pn.Row(react_mpl_plot_weight, pn.Column(pn.Spacer(height=30),react_pandasBokeh_plot_weight))
tab2 = pn.Column(bokeh_plot)
tabs = pn.Tabs(("MPL/pandasBokeh", tab1), ("Bokeh linked brushing demo", tab2))
#pn.Column(pn.Row(title, xyWid, height=100), tabs)

# Using .show() to start a Bokeh server instance from within your jupyter notebook for rapid prototyping
# pn.Column(pn.Row(title, xyWid, height=100), tabs).show(title="Auto Analysis with .show")

# Using .servable() to turn a notebook into a deployable app
pn.Column(pn.Row(title, xyWid, height=100), tabs).servable(title="Auto Bokeh: Tabs/linked brushing")


# ### Pushing changes after the initial setup

# Once this initial setup for your app is done, each time you make changes to any of your code/data and other setup files, you just need to execute the following four commands:
# - Add and commit your application code to the git
# >	git add .  <br>
# >	git commit -m “myviz”
# - Deploy your code
# >	git push heroku main 
#     - For some of you depending on how your head refs was initially set up, your "main" branch may be called "master". So you may need to use 
#     > git push heroku master <br>
#     > Better yet, I would urge you all to consider renaming the branch to 'main'. See [why](https://www.zdnet.com/article/github-to-replace-master-with-main-starting-next-month/) and [how](https://github.com/github/renaming) of renaming. 
# 
# - Launch the app
# >	heroku open
# 
# - Check the log file for any error messages
# >	heroku logs --tail

# # Practice Exercises:
#     
# - Can you make visual styling changes to the 2nd scatterplot so that it is consistent with the first bokeh scatterplot?
# - After making these changes push them back to your heroku server?
