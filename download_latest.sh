#!/bin/bash
curl 'http://osmc.noaa.gov/erddap/tabledap/OSMC_30day.csv?platform_code%2Cplatform_type%2Ccountry%2Ctime%2Clatitude%2Clongitude%2Cobservation_depth%2Csst%2Catmp%2Cprecip%2Cztmp%2Czsal%2Cslp%2Cwindspd%2Cwinddir%2Cwvht%2Cwaterlevel%2Cclouds%2Cdewpoint%2Cuo%2Cvo%2Cwo%2Crainfall_rate%2Chur%2Csea_water_elec_conductivity%2Csea_water_pressure%2Crlds%2Crsds%2Cwaterlevel_met_res%2Cwaterlevel_wrt_lcd%2Cwater_col_ht%2Cwind_to_direction%2Clon360&time%3E=2020-05-31T00%3A00%3A00Z' -o refresh.csv
if [ $? -eq 0 ]
then
  mv refresh.csv latest.csv
else
  echo "Could not latest observations from GTS ERDDAP"
fi
