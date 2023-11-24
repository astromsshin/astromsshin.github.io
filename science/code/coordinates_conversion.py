#! /usr/bin/env python

###### Convert formats of coordinates ######
##   Min-Su Shin (University of Michigan) ##
############################################

import string, fpformat, sys

def deg2str_dms(deg):
	if deg < 0.0 :
		sign="-"
		deg = -1.0*deg
	else:
		sign="+"
	deg_temp = int(deg)
	str_deg = str(deg_temp)
	temp = (deg - int(deg))*3600.0
	min = int(temp/60)
	str_min = str(min)
	str_sec = str(fpformat.fix((deg*3600.0 - deg_temp*3600.0 - 60.0*min),1))
	final_str = sign+str_deg.zfill(2)+":"+str_min.zfill(2)+":"+str_sec.zfill(4)
	return final_str

def deg2str_hms(deg):
	deg = deg/15.0
	hour_temp = int(deg)
	str_hour = str(hour_temp)
	temp = (deg - int(deg))*3600.0
	min = int(temp/60)
	str_min = str(min)
	str_sec = str(fpformat.fix((deg*3600.0 - hour_temp*3600.0 - 60.0*min),2))
	final_str = str_hour.zfill(2)+":"+str_min.zfill(2)+":"+str_sec.zfill(5)
	return final_str

def hms2str_deg(hms):
	temp = string.split(hms, ":")
	h = float(temp[0])
	m = float(temp[1])
	s = float(temp[2])
	temp = 15.0 * (h + m / 60.0 + s / 3600.0)
	final_str = "%f" % (temp)
	return final_str

def dms2str_deg(hms):
	temp = string.split(hms, ":")
	d = float(temp[0])
	m = float(temp[1])
	s = float(temp[2])
	if d < 0.0 :
		temp = d - m / 60.0 - s / 3600.0
	else :
		temp = d + m / 60.0 + s / 3600.0
	final_str = "%f" % (temp)
	return final_str



if len(sys.argv) < 3:
	print "(usage) %s (RA) (DEC)" % (sys.argv[0])
	print "ex) %s 23:01:23.3 -24:00:02.3" % (sys.argv[0])
	print "ex) %s 321.345 -25.6839" % (sys.argv[0])
	sys.exit()

temp = string.split(sys.argv[1], ":")
if len(temp) < 2 :
	in_ra = float(sys.argv[1])
	in_dec = float(sys.argv[2])
	print deg2str_hms(in_ra), deg2str_dms(in_dec)
else:
	in_ra = sys.argv[1]
	in_dec = sys.argv[2]
	print hms2str_deg(in_ra), dms2str_deg(in_dec)
