#!/usr/bin/env bash

########
#script for running analysis with JPET framework
########

confpath=/home/jpet/pliki_szymona/configs
nfiles=100
njobs=8

# options commented out
#               -p $confpath/conf_djpet.xml \
#               /data/3/users/alek/FTAB/Imaging/framework/examples/Imaging/Imaging.x \
#                /data/3/users/alek/FTAB/Imaging/framework/kitt_build/examples/Imaging/Imaging.x \
find . -name \*hld \
    | head -n $nfiles \
    | parallel -j $njobs \
               ~/examples-build/ModularDetectorAnalysis/ModularDetectorAnalysis.x \
               -t hld \
               -k modular \
               -p $confpath/conf_djpet.xml \
               -u $confpath/params.json \
               -l $confpath/ccb_setup_thresholds_ds.json -i 36  \
               -d \
	       -f



