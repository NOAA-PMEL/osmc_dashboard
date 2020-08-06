#!/usr/bin/env python
# coding: utf-8

# This is the current version.
# 
# Running with an ERDDAP URL was many time slower to load.
# 
# This version does each plot individually and composes them in a GridSpec panel.

# In[77]:


import pandas as pd
import utility as u
import numpy as np
import datetime
import colorcet as cc


# In[78]:


df = pd.read_csv('latest_surface.csv', skiprows=[1], low_memory=False)
df.sort_values(['time','observation_depth'], ascending=False, inplace=True)


# In[79]:


# Remove any row that has no surface observation for the 7 surface variables we are plotting.
surface_cols = ('latitude', 
                 'longitude', 
                 'time', 
                 'observation_depth', 
                 'platform_type', 
                 'platform_code', 
                 'sst', 
                 'slp',
                 'atmp',
                 'winddir',
                 'windspd',
                 'dewpoint',
                 'clouds')

# Some platforms report ztmp with observation_depth = 0.0 which is really sst.
# So to get all surface obs you have to segment by platform type
surface_platforms = ['TROPICAL MOORED BUOYS',
                     'C-MAN WEATHER STATIONS',
                     'DRIFTING BUOYS (GENERIC)',
                     'ICE BUOYS',
                     'MOORED BUOYS (GENERIC)',
                     'RESEARCH',
                     'SHIPS (GENERIC)',
                     'SHORE AND BOTTOM STATIONS (GENERIC)',
                     'TIDE GAUGE STATIONS (GENERIC)',
                     'TSUNAMI WARNING STATIONS',
                     'UNKNOWN',
                     'UNMANNED SURFACE VEHICLE',
                     'VOLUNTEER OBSERVING SHIPS',
                     'VOLUNTEER OBSERVING SHIPS (GENERIC)',
                     'VOSCLIM',
                     'WEATHER AND OCEAN OBS',
                     'WEATHER BUOYS',
                     'WEATHER OBS']

# Removes rows with other platform types
surface = df[df.platform_type.isin(surface_platforms)]
# Removes columns that are not metdadata or a desired surface variable
surface = surface.loc[:, surface_cols]
# Removes any row that does not have at least 1 surface observation that is not NaN
surface.dropna(subset=['sst', 'slp', 'atmp', 'winddir', 'windspd', 'dewpoint', 'clouds'], how='all', inplace=True)


# In[80]:



# In[81]:


surface_max = surface.drop_duplicates(['platform_code'])


# In[82]:


surface_locs = surface_max.loc[:,('latitude', 'longitude', 'platform_type', 'platform_code')]
surface_locs.sort_values(['platform_type'], inplace=True)


# In[83]:


# Make time the index for the surface data since all plots are timeseries.
surface['time_val'] = surface['time']
surface.loc[:, 'time'] = pd.to_datetime(surface['time'])
surface.set_index('time', inplace=True)


# In[84]:



# In[85]:


surface_locs.to_pickle('surface_locations_latest.pkl')
surface.to_pickle('surface_data_latest.pkl')

