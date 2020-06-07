# osmc_dashboard (It's live in [public beta](https://ferret.pmel.noaa.gov/osmc/dashboard))
This is an implementation of a data dashboard for the Ocean Systems Monitoring System built on Holoviz.

This repository contains the entire workflow for preparing the data and displaying it using the dashboard.

The data repositry is an internal ERDDAP server, but you can adapt the script (download_latest.sh) to pull data from the [public OSMC server](http://osmc.noaa.gov/erddap/tabledap/OSMC_30day.html).

The steps for deploying are:

1. Install the holoviz conda environment (conda env create -f environment.yml)
1. Download CSV of the latest data (download_latest.csv).
1. Run the ReadWrite.py. This reads the CSV the data and writes out binary pkl files: depth_data_latest.pkl, depth_locations_latest.pkl,  surface_data_latest.pkl, surface_locations_latest.pkl.  This process removes any missing data and organizing point data into surface timeseries (surface_data_latest.pkl) and profile collections (depth_data_latest.pkl) and depth and surface platform most recently reported locations for each platform (depth_locations_latest.pkl, surface_locations_latest.pkl).
1. Serve the dashboard (see: run.sh).

The dashboard code itself is none other than dashboard.ipynb which you can run locally by starting a jupyter server which is included in the conda environment. (I.e. run the command "jupyter notebook" in the notebook directory).
