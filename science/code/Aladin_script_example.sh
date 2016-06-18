#!/bin/bash

# Aladin JAR file PATH
ALADINJAR="/n/Users/msshin/Astro_tools/Aladin.jar" 

# the input file of coordinates which have three columns
# column 1 : object ID (which is not necessary, but is used to find JPEG filenames.)
# column 2 : object RA
# column 3 : object DEC
infn="FIRST.catalog"

# delete JPEG images in the current directory
rm -f ./*.jpg

inid=[]
i=0
for id in `cut -d' ' -f1 $infn`
do
	inid[$i]=$id
	i=$((i+1))
done

RAs=[]
i=0
for id in `cut -d' ' -f2 $infn`
do
	RAs[$i]=$id
	i=$((i+1))
done

DECs=[]
i=0
for id in `cut -d' ' -f3 $infn`
do
	DECs[$i]=$id
	i=$((i+1))
done

i=$((i-1))
for ind in `seq 0 $i`
do

use_id=${inid[$ind]}
use_ra=${RAs[$ind]}
use_dec=${DECs[$ind]}
pic_fn="./"$use_id".jpg"
echo $use_id $pic_fn

# The following example plot DSS2 images from the ESO server, 
# FIRST and XID-II catalogs from Vizier, and Simbad objects. It 
# zooms in 4x, and draws a circle of radius 10" around the 
# given coordinate. The plots are saved as JPEG files.
# If you want to find other features of Aladin, please, 
# check Aladin manual 
# http://aladin.u-strasbg.fr/java/AladinManual6.pdf
# and FAQ web site
# http://aladin.u-strasbg.fr/java/FAQ.htx
java -jar $ALADINJAR -nogui -nobanner -noreleasetest -nohub << ends
get ESO(DSS2) $use_ra $use_dec
get Vizier(FIRST) $use_ra $use_dec
get Simbad $use_ra $use_dec
get Vizier(XID-II) $use_ra $use_dec
sync
zoom 4x
draw circle("$use_ra" "$use_dec" 10arcsec)
sync
save -jpg100 $pic_fn
quit
ends

done
