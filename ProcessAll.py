#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
import colorcet as cc


# In[2]:


df = pd.read_csv('latest.csv', skiprows=[1])
df.sort_values(['platform_code','time','observation_depth'], ascending=False, inplace=True)


# In[3]:


# Drops any row that does not have at least one data column with valid value
df.dropna(subset=['sst', 'slp', 'atmp', 'winddir', 'windspd', 'dewpoint', 'clouds', 'ztmp', 'zsal'], how='all', inplace=True)
platform_locations =  df.drop_duplicates(['platform_code'])
platform_locations


# In[4]:


platform_locations = platform_locations.loc[:,('latitude', 'longitude', 'platform_type', 'platform_code')]
platform_locations.sort_values(['platform_type'], inplace=True)
platform_locations


# In[5]:


df['time_val'] = df['time']
df.loc[:, 'time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)


# In[6]:


platform_locations.to_pickle('locations_latest.pkl')
df.to_pickle('data_latest.pkl')

