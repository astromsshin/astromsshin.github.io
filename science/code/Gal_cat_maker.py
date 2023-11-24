#!/bin/env python

# Making a catalog of galaxies which are included in given target fields
# This was made for Myung-Jun Kim by Min-Su Shin (astroshin@yonsei.ac.kr)
# Department of Astronomy, Yonsei University, Seoul, Korea

# field list file of 5 cols
# col 1 : field number
# col 2 : center RA
# col 3 : center DEC
# col 4 : width of RA
# col 5 : width of DEC

# galaxy list file with RA(3 col), DEC(4 col)
# col 1 : anything
# col 2 : anything
# col 3 : galaxy RA
# col 4 : galaxy DEC

# CAUTION : both the galaxy list file and the target field file should be sorted 
# by the dec. in the ascending order before it is used by this program.

# ASSUMPTION : the target fields are parallel to an equatorial line.

import string, sys
if(len(sys.argv) != 3) :
	print "Usage: Gal_cat_maker.py [field list file of at least 5 cols] [galaxy list file with RA(3 col), DEC(4 col)]"
	sys.exit()
targetfn = sys.argv[1]
input_fld = open(targetfn, 'r')
galaxyfn = sys.argv[2]
input_gal = open(galaxyfn, 'r')

# Reading the first line of TF file
line_one = input_fld.readline()
temp = string.split(line_one)
tfgalfn = "TF"+temp[0]+".gal"
tfRA = float(temp[1])
tfDEC = float(temp[2])
PREtfDEC = tfDEC
deltaRA=float(temp[3])
deltaDEC=float(temp[4])
sameDECnum=0
gal_line_one=""
while 1:
	check_ind=1
	cutRAl=tfRA-deltaRA/2.0
	cutRAu=tfRA+deltaRA/2.0
	cutDECl=tfDEC-deltaDEC/2.0
	cutDECu=tfDEC+deltaDEC/2.0
	output_gal = open(tfgalfn, 'w')
	output_gal.write(str(tfRA)+" "+str(tfDEC)+"\n")
	output_gal.write(str(cutRAl)+" "+str(cutRAu)+" "+str(cutDECl)+" "+str(cutDECu)+"\n")
	print tfgalfn
	if( tfDEC != PREtfDEC ) :
		if(galDEC <= cutDECu) :
			if( (cutRAl >= 0) and (cutRAu <= 24.0) ) :
				if( (cutRAl <= galRA) and (cutRAu >= galRA) and (cutDECl <= galDEC) and (cutDECu >= galDEC)) :
					output_gal.write(gal_line_one)
			else:
				cutRAu = cutRAu - 24.0
				if( (cutRAl <= galRA) and (cutRAu >= galRA) and (cutDECl <= galDEC) and (cutDECu >= galDEC)) :
					output_gal.write(gal_line_one)
	else :
		sameDECnum=sameDECnum+len(gal_line_one)
		input_gal.seek(-1*sameDECnum, 1)
	sameDECnum=0
	# Reading the possible lines of a galaxy list file
	while(check_ind > 0) :
		gal_line_one = input_gal.readline()
		if not gal_line_one:
			break
		tline = string.split(gal_line_one)
		GALRA=tline[2]
		GALDEC=tline[3]
		galRA=float(GALRA)
		galDEC=float(GALDEC)
		if(galDEC <= cutDECu) :
			sameDECnum=sameDECnum+len(gal_line_one)
			if( (cutRAl >= 0) and (cutRAu <= 24.0) ) :
				if( (cutRAl <= galRA) and (cutRAu >= galRA) and (cutDECl <= galDEC) and (cutDECu >= galDEC)) :
					output_gal.write(gal_line_one)
			else:
				cutRAu = cutRAu - 24.0
				if( (cutRAl <= galRA) and (cutRAu >= galRA) and (cutDECl <= galDEC) and (cutDECu >= galDEC)) :
					output_gal.write(gal_line_one)
		else :
			check_ind = 0
			output_gal.close()
			PREtfDEC = tfDEC
	line_one = input_fld.readline()
	if not line_one:
		break
	temp = string.split(line_one)
	tfgalfn = "TF"+temp[0]+".gal"
	tfRA = float(temp[1])
	tfDEC = float(temp[2])
	deltaRA=float(temp[3])
	deltaDEC=float(temp[4])

input_fld.close()
input_gal.close()
