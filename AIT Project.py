#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Set up
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as pltiker
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
from datetime import datetime
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter

df = pd.read_csv("Desktop/School Work/Graduate/Fall 2021/AIT 580/Project/NYC_CRIME_2014.csv")


# In[3]:


#Manipulation
df['DATE'] = pd.to_datetime(df.DATE)
print(df.dtypes)


# In[4]:


#Structure
index = df.index
rows = len(index)
print('The amount of rows in this data frame is: ')
print(len(index))
dates = df.groupby(['DATE']).size()
gender = df.groupby(['Vict Sex']).count()


# In[5]:


#Total Crime plot count
date_form = DateFormatter('%b')
fig, ax = plt.subplots(figsize=(18,12))
ax.plot(dates, color = 'black')
#New Year line
ax.axvspan(date2num(datetime(2014,1,1)), date2num(datetime(2014,1,1)),
          label = 'New Years', color = 'red', alpha=10)
#4th line
ax.axvspan(date2num(datetime(2014,7,4)), date2num(datetime(2014,7,4)),
          label = '4th of July', color = 'blue', alpha=10)
#Thanksgiving line
ax.axvspan(date2num(datetime(2014,11,27)), date2num(datetime(2014,11,27)),
          label = 'Thanksgiving', color = 'green', alpha=10)
#Christmas
ax.axvspan(date2num(datetime(2014,12,25)), date2num(datetime(2014,12,25)),
          label = 'Christmas', color = 'orange', alpha=10)
ax.xaxis.set_major_formatter(date_form)
ax.legend()
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.title('Number of Crimes for L.A. in 2014')
plt.xlabel('Date')
plt.ylabel('# of Crime')
plt.show()


# In[ ]:




