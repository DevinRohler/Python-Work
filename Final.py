#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Devin Rohler (G01080595)
import os
os.getcwd()


# In[12]:


#setup
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily 
import mapclassify
import matplotlib.ticker as pltiker
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
#read in
covid = pd.read_csv("C:\\Users\\Devin\\Desktop\\School Work\\Spring 2021\\MIS 433\\Project\\project_covid19.csv")
covid.copy()


# In[13]:


#Question 1 
#apply sum to last date
covid_drop_columns = covid.drop(['UID','iso2','iso3','code3',
                                 'FIPS','Lat',"Long_"],axis=1)
covid_drop_dates = covid_drop_columns.drop(covid.iloc[:,11:467],axis=1)
print('The total number of Covid19 cases in the US up to April 22 2021 is: ')
print(covid_drop_dates['4/22/21'].sum())


# In[14]:


#Question 2 

#subset virginia and apply sum to last date 
covid_va = covid_drop_dates[covid_drop_dates['Province_State'] == 'Virginia']
print('The total number of Covid19 cases in Virginia up to April 22 2021 is: ')
print(covid_va['4/22/21'].sum())


# In[15]:


#Question 3
#drop columns
covid_va_3 = covid_drop_columns[covid_drop_columns
                                ['Province_State'] == 'Virginia']
covid_va_3_drop = covid_va_3.drop(covid_va_3.iloc[:,4:-10],axis=1)

#melt
covid_va_melt = covid_va_3_drop.melt(id_vars=
    ['Admin2','Province_State','Country_Region',
                                             'Combined_Key'],
                                    var_name = 'dates',
                                    value_name = 'cases')

#group by & create new variable
past10 = covid_va_melt.groupby(['dates']).sum()
past10['newcases'] = past10['cases'].diff()


#plot
fig1 = plt.figure(figsize = (12,8))
plt.bar(past10.index,past10['newcases'], data = past10)

plt.ylabel("New Cases")
plt.title('Virginia - New Covid19 Cases ')
plt.show()


# In[16]:


#Question 4    
#group by and max
covid_va_4 = covid_va.groupby(["Admin2"]).sum()
print('Fairfax reported the highest amount of total cases: ')
print(covid_va_4[covid_va_4['4/22/21']==covid_va_4['4/22/21'].max()])


# In[17]:


#Question 5  #
#Melt
covid_va_5 = covid_drop_columns[covid_drop_columns['Combined_Key'] == 'Fairfax, Virginia, US']
covid_va_5_melt = covid_va_5.melt(id_vars=['Admin2',
                                'Province_State','Country_Region',
                                        'Combined_Key'],
                                    var_name = 'dates',
                                    value_name = 'cases')
#create new column and max
covid_va_5_melt['newcases'] = covid_va_5_melt['cases'].diff()
print(covid_va_5_melt[covid_va_5_melt['newcases'] ==covid_va_5_melt['newcases'].max()])
print('Fairfax county produced the most new cases on 1/17/21 with 1485 new cases')


# In[18]:


#Question 6 

#create variables, and melt
start = '3/1/21'
end = '3/31/21'
Fairfax_new = covid_drop_columns[covid_drop_columns['Combined_Key'] == 'Fairfax, Virginia, US']
Fairfax_melt = Fairfax_new.melt(id_vars=['Admin2','Province_State','Country_Region',
                                             'Combined_Key'],
                          var_name = 'dates',
                          value_name = 'cases')

#to date time, make date condition, create new column
Fairfax_melt['dates'] = pd.to_datetime(Fairfax_melt['dates'])
Fairfax_melt = Fairfax_melt[(Fairfax_melt['dates'] >= start) & (Fairfax_melt['dates'] <= end)]
Fairfax_melt['newcases'] = Fairfax_melt.iloc[:,5].diff()

#print results
print('Average new cases per day in Fairfax, VA for the month of March 2021: ')
print(Fairfax_melt['newcases'].sum()/len(Fairfax_melt['newcases']))
print('Average new cases per day in Fairfax, VA for the month of March 2021: ')
print(Fairfax_melt['newcases'].sum())


# In[19]:


#Question 7

#subset Arlington and Fairfax with query
ffx_ar = covid_drop_columns.query("Combined_Key == 'Fairfax, Virginia, US'or Combined_Key == 'Arlington, Virginia, US'")
ffx_ar_drop = ffx_ar.drop(ffx_ar.iloc[:,0:3],axis=1)

#melt to get cases
ffx_ar_melt = ffx_ar_drop.melt(id_vars=['Combined_Key'],
                         var_name = 'dates',
                         value_name = 'cases')
#plot
plt.figure(figsize = (12,8))
sns.lineplot(x = 'dates',y = 'cases', hue = "Combined_Key", data = ffx_ar_melt)
plt.title("Covid19 Cases From Beginning To Current Date")
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(60))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(30))
plt.show()


# In[28]:


#Part2
#read in country geometry
zipfile = "zip:///Users//Devin//Desktop//School Work//Spring 2021//MIS 433//Project//counties(2).zip"
usa = gpd.read_file(zipfile)
gdf = covid
gdf = gpd.GeoDataFrame(gdf, 
                       crs = "EPSG:4326", 
                       geometry = gpd.points_from_xy(gdf.Long_,gdf.Lat))

#Remove 0 lat & Subset Virginia
gdf[gdf.Lat ==0]['Admin2'].values
gdf = gdf[gdf.Admin2 != "Unassigned"].copy()
gdf = gdf[gdf.Admin2.str.contains("Out ") == False].copy()
gdf = gdf[gdf.Admin2.str.contains("Correction") == False].copy()
gdf[gdf.Lat == 0]['Admin2'].values
v1 = gdf[gdf['Province_State'] == 'Virginia']
v1

#pull virginia counties from usa & rename for merge
virginia = usa.iloc[2785:2889,:]
virginia.rename(columns={'FIPS_BEA':'FIPS'},inplace = True)

#Merge virginia and gdf based on FIPS
v1.drop('geometry',axis = 1,inplace = True)
merge = pd.merge(v1,virginia, on ='FIPS')

#plot
#
fig, ax = plt.subplots(figsize=(20,8))
merge.plot(ax = ax,
       legend = True,
       column = '4/15/20',
       cmap = 'coolwarm',
       figsize=(12,8))
plt.title('Covid cases in Virginia by county, April 15th 2020')
plt.axis("off")
contextily.add_basemap(ax,crs=usa.crs.to_string())
plt.show()
fig, ax = plt.subplots(figsize=(20,8))
merge.plot(ax = ax,
       legend = True,
       column = '4/15/21',
       cmap = 'coolwarm',
       figsize=(12,8))
plt.axis('off')
plt.title('Covid cases in Virginia by county, April 15th 2021')
contextily.add_basemap(ax, crs=usa.crs.to_string())
plt.show()


# In[449]:


#Original Map before 4/27 update
fig, ax = plt.subplots(figsize=(12,8))
v2.plot(ax=ax,
       column = '4/15/20',
       legend = True,
       cmap ='coolwarm')
plt.axis('off')
contextily.add_basemap(ax, crs=usa.crs.to_string())
plt.show()


# In[151]:


fig, ax = plt.subplots(figsize=(12,8))
v2.plot(ax=ax,
       column = '4/15/21',
        cmap='coolwarm',
       legend = True)
contextily.add_basemap(ax, crs=usa.crs.to_string())
plt.show()


# In[ ]:




