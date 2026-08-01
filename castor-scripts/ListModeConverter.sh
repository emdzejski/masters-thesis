#!/usr/bin/env bash

######
#script for conversion of JPET framework analysis .root files to castor format
######
confpath=/home/jpet/pliki_szymona/configs
executable=/home/jpet/examples-build/ListmodeExport/ListmodeExport.x


$executable \
           -t root \
           -k modular \
           -p $confpath/conf_djpet.xml \
           -u $confpath/imaging_params.json \
           -l $confpath/ccb_setup_thresholds_ds.json -i 36  \
           -d \
           -f "$@" -b


