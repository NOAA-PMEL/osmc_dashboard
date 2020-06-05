#!/usr/bin/env python
# coding: utf-8

# In[45]:


import pandas as pd
import numpy as np


# In[46]:


depth = pd.read_pickle('depth_data_latest.pkl')
surface = pd.read_pickle('surface_data_latest.pkl')
depth_locs = pd.read_pickle('depth_locations_latest.pkl')
surface_locs = pd.read_pickle('surface_locations_latest.pkl')


# In[47]:


dnames = list(depth['platform_type'].unique())
snames = list(surface['platform_type'].unique())
names = dnames + snames
print("\nAll platform types reporting:\n")
all = sorted(set(names))
print(*all, sep='\n')


# In[48]:


print("\nNumber of Depth Platforms:\n")


# In[49]:


counts = depth_locs['platform_type'].value_counts()
print(counts.to_string())


# In[50]:


print('\nNumber of Surface Platforms:\n')
scounts = surface_locs['platform_type'].value_counts()
print(scounts.to_string())


# In[55]:


print("\nNumber of Observations:")
print("\nDepth Platforms:\t" + format(depth.shape[0],',d'))
print("Surface Platforms:\t" + format(surface.shape[0],',d'))

