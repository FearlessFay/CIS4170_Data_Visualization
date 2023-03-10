#!/usr/bin/env python
# coding: utf-8

# How many athletes from each country participated in 2016? Show only top 20 countries.
# How many medals for each country? Can you create a breakdown based on the type of medal? 


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'notebook')


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


olyDF = pd.read_excel(r"D:\2022Fall\Data Visualization\Olympics2016.xlsx")
olyDF

olyFig, olyGrid = plt.subplots(2, figsize=(30,18))
olyFig.suptitle("Analyzing 2016Olympics dataset", fontsize=15)
olyFig.subplots_adjust(wspace=.5, hspace=.5)


atheletsCnt = olyDF.groupby(by='NOC').size()
atheletsCnt_S = atheletsCnt.iloc[0:]
atheletsCnt_S1 = atheletsCnt_S.sort_values()
print(atheletsCnt_S1)

# athCNT = oDF.groupby(['Team']['ID']).nunique().nlargest(20).reset_index()
# athCNT


atheletsCnt_S2 = atheletsCnt_S1[-21:-1]
print(atheletsCnt_S2)


atheletsCnt_S2.plot.barh(ax=olyGrid[0], title="# of athelets by countries") 

print(atheletsCnt_S2)


# medalCnt = pd.crosstab(olyDF.NOC, olyDF.Medal, margins=True).reset_index().sort_values(by="All")
# print(medalCnt)


medalCnt1 = pd.crosstab(olyDF.NOC, olyDF.Medal, margins=True).sort_values(by="All")
print(medalCnt1)
type(medalCnt1)


medalCnt1[-21:-1].plot.barh(ax=olyGrid[1], title="# of medals(breakdown) by countries")
