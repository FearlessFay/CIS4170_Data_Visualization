#!/usr/bin/env python
# coding: utf-8

# # Visualizing with pandas

# In[20]:


# To display the output of plotting commands inline within frontends like the Jupyter notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# To add some basic interaction to the matplotlib charts
get_ipython().run_line_magic('matplotlib', 'notebook')


# In[21]:


# importing all the needed libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn


# In[22]:


plotDF = pd.DataFrame(np.random.rand(15, 5).cumsum(0), # Create 15x5 dataframe of randomly generated numbers that are cumulatively added up
                      columns = ['AAPL','BOA','COST','DEC','FB'], # specify column names as a list
                      index=pd.date_range('1/1/2020', periods=15)) # create a date-based index
plotDF.index = plotDF.index.to_period('D')
print(plotDF)


# In[23]:


# First create the subplots with matplotlib, and then plot on a specific subplot by specifying the 'ax' keyword

# This will create a 2x2 grid of subplots and return the figure container (fig) and list of subplots (dfGrid).
fig, dfGrid = plt.subplots(2, 2, figsize=(12,8))

# Add padding space around the subplots 
# Complete call signature: plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
fig.subplots_adjust(wspace=.4, hspace=.4)
# fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)

# Bar chart will be added in the top left corner by specifying ax=dfGrid[0,0] 
plotDF.plot(kind='bar', ax=dfGrid[0,0])
dfGrid[0,0].set_xticklabels(labels=plotDF.index, rotation=30, fontsize='small')

plotDF.AAPL.plot(kind='bar', ax=dfGrid[0,1])

plotDF[['AAPL','BOA']].plot(kind='bar', ax=dfGrid[1,0])


# In[ ]:


#dfGrid[0,0].cla()


# In[24]:


# When plotting a single column
#dfGrid[0,1].cla()
plotDF.BOA.plot(kind='barh', ax=dfGrid[1,1])


# #### In-class Practice exercises
# 1. In the last session, we created plots using all of the columns in the dataset (except for plot # 3). What if we wanted to create a plot using only some of the columns?

# In[ ]:


# Line chart in top right
plotDF.plot(kind='line', ax=dfGrid[0,1])

# histogram for values in column AAPL in bottom left
plotDF.AAPL.plot(kind='hist', ax=dfGrid[1,0])

# Horizontal stacked bar chart in bottom right
plotDF.plot(kind='barh', stacked=True, ax=dfGrid[1,1])


# In[ ]:


# When plotting two or more columns
dfGrid[0,0].cla()
plotDF[['AAPL','DEC']].plot(kind='barh', ax=dfGrid[0,0])


# #### For more detailed guide on creating quick visualizations using pandas refer to https://pandas.pydata.org/pandas-docs/dev/user_guide/visualization.html

# # Let's work through a dataset to create visualizations with pandas

# ## A 5-step process to creating visualizations
# - What is the question that you will be willing to explore?
# - What variable(s) you will need to use? This will greatly drive the kind of visualization you should use 
# - Organize your views. You will need more than one view to identify and discern interesting insights 
# - Prepare your data. This will be the most time-consuming step (and has nothing to do with visualization itself!)
# - Plot your data

# #### Valuable pandas commands to slice-and-dice your data
# 1. pd.groupby()
# 2. pd.crosstab()
# 3. pd.pivot_table()

# In[15]:


tipsDF = pd.read_excel("tips.xlsx")
tipsDF


# In[26]:


# Create the figure and subplots 
tipFig, tipGrid = plt.subplots(2,2, figsize=(10,6))
# IF you would like to customize the grid layout further, refer to https://matplotlib.org/3.1.0/tutorials/intermediate/gridspec.html

# Add the title for the figure container
tipFig.suptitle("Analyzing tips dataset", fontsize=15)

# Adjusting the padding space around subplots
tipFig.subplots_adjust(wspace=.5, hspace=.5)



# In[27]:


# 1. Number of parties by day
dayCnt = pd.crosstab(tipsDF.day, tipsDF.time)
print(dayCnt)
dayCnt.plot.barh(ax=tipGrid[0,0], title="Number of parties by day")


# In[ ]:


# 2. How many parties were categorized as smoking vs. non-smoking diners? Create a bar chart to show this visually
smokeCnt = pd.crosstab(tipsDF.day, tipsDF.smoker)
print(smokeCnt)
smokeCnt.plot.bar(ax=tipGrid[0,1],color=['green', 'red'], width=.5)

# Setting the properties using set_title and dictionary approach
smokeDT = {'title':"# of smoking parties by day",
           'xlabel':'day of the week',
           'ylabel':'count'}

tipGrid[0,1].set(**smokeDT)


# In[ ]:


# 3. Create an histogram with 10 bins for Tip% 
# First, calculate the % of tip that was paid as part of the total bill and add that as a column to your existing DF
tipsDF['tipPCT'] = tipsDF['tip']/tipsDF['total_bill'] * 100
tipsDF


# In[ ]:


# Now Plot the histogram and set the gridlines to false

tipGrid[1,0].cla()
tipsDF.tipPCT.hist(bins=10,  ax=tipGrid[1,0])
tipGrid[1,0].grid(False)
tipsDT = {'title':'Frequency of tipping %', 
          'xlabel':'Tip %'}
tipGrid[1,0].set(**tipsDT)


# In[ ]:


# 4. # of parties by the size of the party

day = pd.crosstab(tipsDF['day'], tipsDF['size']) 
print(day)
day.plot.bar(ax=tipGrid[1,1], title='# of parties by the size of the party', 
             xlabel="day of the week")
tipGrid[1,1].legend(loc="upper left", ncol=len(day.columns),fontsize=7)


# ### Clearing plot space
# 
# - plt.cla(): To clear a subplot 
# - plt.clf(): To clear an entire figure (Careful as this will clear and remove all the subplots too)

# In[ ]:


# Clearing plot space

#plt.cla(): To clear a subplot 
tipGrid[1,0].cla()

#plt.clf(): To clear an entire figure (Careful as this will clear and remove all the subplots too)
#tipFig.clf()

