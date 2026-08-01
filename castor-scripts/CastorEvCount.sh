#!/usr/bin/env bash

############
#script for creating a castor header file (.Cdh) for a merged data file (.Cdf) 
############

total_events=$(grep -h "Number of events:" *.Cdh | awk '{sum+=$4} END {print sum}')

#take the first header file as a template
first_header=$(ls *.Cdh | head -n 1)

cp "$first_header" DJ_2021.10.24_0004_merged.Cdh

#using 'sed' to update the master metadata values
sed -i "s/Data filename:.*/Data filename: DJ_2021.10.24_0004_merged.Cdf/g" DJ_2021.10.24_0004_merged.Cdh
sed -i "s/Number of events:.*/Number of events: $total_events/g" DJ_2021.10.24_0004_merged.Cdh

echo "--------------------------------------------------------"
echo " -> Binary Data: DJ_2021.10.24_0004_merged.Cdf"
echo " -> ASCII Header: DJ_2021.10.24_0004_merged.Cdh (Total Events: $total_events)"
echo "--------------------------------------------------------"