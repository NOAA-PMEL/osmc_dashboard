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

#need to add data types to this read to avoid error
df = pd.read_csv('latest_depth.csv', dtype={'platform_code': "string", 'platform_type':"string", 'latitude':"float64", 'observation_depth':"float64"},skiprows=[1])
df.sort_values(['time','observation_depth'], ascending=False, inplace=True)

#pull the location values from second csv file
df_surface_locs =  pd.read_csv('latest_depth_locs.csv', dtype={'platform_code': "string", 'platform_type':"string", 'latitude':"float64", 'observation_depth':"float64"},skiprows=[1])
df_surface_locs.sort_values(['platform_type'], ascending=True, inplace=True)


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



df_surface_locs.to_pickle('depth_locations_latest.pkl')
depth.to_pickle('depth_data_latest.pkl')

