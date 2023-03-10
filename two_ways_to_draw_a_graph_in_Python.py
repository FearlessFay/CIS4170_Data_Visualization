#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'notebook')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn

# way 1 to draw a graph 
plt.figure(figsize=(9,7))
plt.plot(np.random.randn(10),np.random.randn(10),
         color='purple',linestyle='dashed',linewidth=2,
         marker='x',markersize=8)

plt.plot([3,4,1,2,8,6,7,8,9,10],'g--')
plt.show()

plt.barh(['Sweden','ROC','Netherlands'],[3,7,5],height=.5)
plt.title('Winter Olympics Total Medal Count')

plt.hist(np.random.randn(50),bins=10,color='blue')

# way 2 to draw a graph
myFig = plt.figure(figsize=(7,5))

myPlot = myFig.add_subplot(2,2,2)
myPlot.bar(['Apple','Banana','Cherry','Dragon fruit'],[10,8,5,12],width=0.5)

myPlot = myFig.add_subplot(2,2,1)
myPlot.bar(['Apple','Banana','Cherry','Dragon fruit'],[10,8,5,12],width=0.5)

myPlot = myFig.add_subplot(2,2,3)
myPlot.bar(['A','B','C','D'],[2,8,3,10],width=0.8)

myPlot = myFig.add_subplot(2,2,3)
myPlot.bar(['A','B','C','D'],[2,8,3,10],width=1.0)

myPlot = myFig.add_subplot(2,2,3)
myPlot.scatter([1,2,3],[1,2,3],color='red')

myFig2 = plt.figure(figsize=(7,5))

myPlot = myFig2.add_subplot(2,2,1)
myPlot.scatter([1,2,3],[1,2,3],color='red')

