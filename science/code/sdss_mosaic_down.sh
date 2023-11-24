#!/bin/bash

# Written by Min-Su Shin, Department of Astrophysical Sciences, Princeton University
# It extracts the SDSS mosaic image from the IRSA web service

fn=$1
echo $1

wget -O temp.htm "http://irsa.ipac.caltech.edu/cgi-bin/FinderChart/nph-finder?locstr=$fn&survey=sdss&subsetsize=6.0"
temp_str=`head -482 temp.htm | tail -1`
test_str=${temp_str:15}
test_str=${test_str%%"\">"}
echo $test_str

wget -O $1.tar $test_str

rm -f temp.htm
