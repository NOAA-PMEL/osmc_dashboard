#!/bin/bash
wget 'http://dunkel.pmel.noaa.gov:8336/erddap/tabledap/osmc_gts.csv?platform_code%2Cplatform_type%2Ctime%2Clatitude%2Clongitude%2Cobservation_depth%2Cztmp%2Czsal%2Csst%2Catmp%2Cslp%2Cwindspd%2Cwinddir%2Cclouds%2Cdewpoint&time%3E=now-14days&latitude<=90&longitude<=180&platform_type!="WEATHER OBS"&platform_type!="WEATHER AND OCEAN OBS"&platform_type!="VOLUNTEER OBSERVING SHIPS"&platform_type!="RESEARCH"' -O refresh.csv
if [ $? -eq 0 ]
then
  mv refresh.csv latest.csv
else
  echo "Could not latest observations from GTS ERDDAP"
fi
