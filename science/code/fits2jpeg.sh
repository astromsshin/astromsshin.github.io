#!/bin/bash

rm -f *.jpg

for fn in `ls *.fits`
do

	fn=${fn%%".fits"}
	echo $fn
	fits_fn=$fn".fits"
	jpeg_fn=$fn".jpg"
	ds9 -cmap b -histequ $fits_fn -wcs align yes -zoom to fit -saveimage jpeg $jpeg_fn -exit

done
