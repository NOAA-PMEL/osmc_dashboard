#!/bin/bash 
eval "$(/home/users/kobrien/miniconda3/bin/conda shell.bash hook)"\

#Surface Data
wget 'http://osmc.noaa.gov/erddap/tabledap/OSMC_30day.csv?platform_code%2Cplatform_type%2Ctime%2Clatitude%2Clongitude%2Cobservation_depth%2Cztmp%2Czsal%2Csst%2Catmp%2Cslp%2Cwindspd%2Cwinddir%2Cclouds%2Cdewpoint&time%3E=now-30days&latitude<=90&longitude<=180&platform_type!="WEATHER OBS"&platform_type!="WEATHER AND OCEAN OBS"&platform_type!="VOLUNTEER OBSERVING SHIPS"&platform_type!="RESEARCH"&orderByClosest("platform_code,time/60mins")' -O refresh.csv
if [ $? -eq 0 ]
then
  mv refresh.csv latest_surface.csv
  python ReadWriteSurface.py
else
  echo "Could not latest observations from GTS ERDDAP"
fi


#First get just the lat/lon positions of all platform reporting with an obs depth> 10m
wget 'http://dunkel.pmel.noaa.gov:8336/erddap/tabledap/osmc_gts.csv?platform_code%2Cplatform_type%2Ctime%2Clatitude%2Clongitude&time%3E=now-30days&observation_depth%3E=10&platform_type!="C-MAn WEATHER STATIONS"&platform_type!="DRIFTING BUOYS (GENERIC)"&platform_type!="MOORED BUOYS (GENERIC)"&platform_type!="ICE BUOYS"&platform_type!="SHIPS"&platform_type!="SHIPS (GENERIC)"&platform_type!="VOLUNTEER OBSERVING SHIPS (GENERIC)"&platform_type!="VOSCLIM"&ztmp>-400&distinct()&orderByMax(%22platform_code%2Ctime%22)' -O latest_depth_locs.csv

#Now grab individual CSV files for the major depth platforms
wget 'http://osmc.noaa.gov/erddap/tabledap/OSMC_30day.csv?platform_code%2Cplatform_type%2Ctime%2Clatitude%2Clongitude%2Cobservation_depth%2Cztmp%2Czsal&time%3E=now-30days&observation_depth%3E=10&platform_type=~"(AUTONOMOUS PINNIPEDS|TROPICAL MOORED BUOYS)"&orderBy("platform_code,time,observation_depth")' -O refresh_buoys_seal.csv
wget 'http://osmc.noaa.gov/erddap/tabledap/OSMC_30day.csv?platform_code%2Cplatform_type%2Ctime%2Clatitude%2Clongitude%2Cobservation_depth%2Cztmp%2Czsal&time%3E=now-30days&platform_type="GLIDERS"&orderByClosest("platform_code,time,observation_depth/.2m")' -O refresh_gliders.csv
wget 'http://osmc.noaa.gov/erddap/tabledap/OSMC_30day.csv?platform_code%2Cplatform_type%2Ctime%2Clatitude%2Clongitude%2Cobservation_depth%2Cztmp%2Czsal&time%3E=now-30days&platform_type="PROFILING FLOATS AND GLIDERS (GENERIC)"&orderByClosest("platform_code,time, observation_depth/.1m")' -O refresh_argo.csv

if [ $? -eq 0 ]
then
    head -2 refresh_buoys_seal.csv > latest_depth.csv
    tail -n +3 -q refresh_buoys_seal.csv >> latest_depth.csv
    tail -n +3 -q refresh_gliders.csv >> latest_depth.csv
    tail -n +3 -q refresh_argo.csv >> latest_depth.csv
    python ReadWriteDepth.py
else
  echo "Could not latest observations from GTS ERDDAP"
fi




scp depth_data_latest.pkl tomcat@new-bock:/home/bock/tomcat/OSMCDashboard/view/depth_data_latest.pkl
scp depth_locations_latest.pkl tomcat@new-bock:/home/bock/tomcat/OSMCDashboard/view/depth_locations_latest.pkl
scp surface_data_latest.pkl tomcat@new-bock:/home/bock/tomcat/OSMCDashboard/view/surface_data_latest.pkl
scp surface_locations_latest.pkl tomcat@new-bock:/home/bock/tomcat/OSMCDashboard/view/surface_locations_latest.pkl
