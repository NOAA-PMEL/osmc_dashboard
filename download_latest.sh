#!/bin/bash
curl 'http://osmc.noaa.gov/erddap/tabledap/OSMC_30day.csv?platform_code%2Cplatform_type%2Ctime%2Clatitude%2Clongitude%2Cobservation_depth%2Cztmp%2Czsal%2Csst%2Catmp%2Cslp%2Cwindspd%2Cwinddir%2Cclouds%2Cdewpoint&time%3E=now-14days&latitude%3C=90&longitude%3C=180&platform_type!=%22WEATHER%20OBS%22&platform_type!=%22WEATHER%20AND%20OCEAN%20OBS%22&platform_type!=%22VOLUNTEER%20OBSERVING%20SHIPS%22&platform_type!=%22RESEARCH%22' -o refresh.csv
if [ $? -eq 0 ]
then
  mv refresh.csv latest.csv
else
  echo "Could not latest observations from GTS ERDDAP"
fi
