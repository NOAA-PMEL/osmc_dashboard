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


df = pd.read_csv('latest.csv', skiprows=[1])
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


depth_platforms = ['TROPICAL MOORED BUOYS',
                   'AUTONOMOUS PINNIPEDS',
                   'CLIMATE REFERENCE MOORED BUOYS',
                   'GLIDERS',
                   'ICE BUOYS',
                   'OCEAN TRANSPORT STATIONS (GENERIC)',
                   'PROFILING FLOATS AND GLIDERS (GENERIC)',
                   'SHORE AND BOTTOM STATIONS (GENERIC)']

# Keep only rows with platforms that report data at depth
depth = df[df.platform_type.isin(depth_platforms)]
# Keep only metadata and depth observation columns (zsal and ztmp)
depth_cols = ('latitude', 'longitude', 'time', 'observation_depth', 'platform_type', 'platform_code', 'zsal', 'ztmp')
depth = depth.loc[:, depth_cols]
# Drop any row that has both ztmp and zsal set to NaN
depth.dropna(subset=['ztmp', 'zsal'], how='all', inplace=True)
# Convert time string to time value, keeping a copy
depth.loc[:, 'time_val'] = depth['time']
depth.loc[:, 'time'] = pd.to_datetime(depth['time'])


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


sort_to_find_surface = depth.sort_values(['time','observation_depth'])
depth_ob_locs = sort_to_find_surface.drop_duplicates(['time'])
depth_max = depth_ob_locs.drop_duplicates(['platform_code'])
depth_locs = depth_max.loc[:,('latitude', 'longitude', 'platform_type', 'platform_code')]
depth_locs.sort_values(['platform_type'], inplace=True)


# In[85]:


depth_locs.to_pickle('depth_locations_latest.pkl')
surface_locs.to_pickle('surface_locations_latest.pkl')
surface.to_pickle('surface_data_latest.pkl')
depth.to_pickle('depth_data_latest.pkl')

