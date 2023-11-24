#!/usr/bin/env python

# Written by Min-Su Shin in Princeton astrophysics
# Feel free use or revise the code.
# puporse : to search the SDSS SpecObjAll in a command-line mode

import sqlcl
import sys
import string
import time
import getopt

if (len(sys.argv) == 1 or len(sys.argv) != 3):
	print "It checks SpecObjAll for a given coordinate and a search radius\n or a photometric ObjID."
	print "usage : sdss_spec_check.py (ra) (dec) -r (search radius) -i (photo ObjID)"
	print "\tra : degree"
	print "\tdec : degree"
	print "\tsearch radius : arcsec (optional) (default : 3 arcsec)"
	print "\tphoto ObjID : SDSS photometric object ID (optional)"
	print "output : SpecObjID plate fiber_id redshift redshift_error SpecClass"
	sys.exit()

search_rad = str(3.0/60.0)
photo_objid = ""
optlist, args = getopt.getopt(sys.argv[1:], 'r:i:')
for o, a in optlist:
	if o == "-r":
		search_rad = str(float(a)/60.0)
	if o == "-i":
		photo_objid = a

if photo_objid == "" :
	ra = sys.argv[1]
	dec = sys.argv[2]
	sql_query = "select P.objid, P.modelMag_u, P.modelMag_g, P.modelMag_r, P.modelMag_i, P.modelMag_z from PhotoObjAll P, dbo.fGetNearbyObjAllEq("+ra+","+dec+","+search_rad+") n where P.objID = n.objID and P.specObjID > 0"
	query_result = sqlcl.query(sql_query).readlines()
	if len(query_result) > 1 :
		data_part = string.split(query_result[1],",")
		photo_objid = data_part[0]
		time.sleep(1.0)
		sql_query = "select S.SpecObjID, S.plate, S.fiberID, S.mjd, S.z, S.zErr, S.specClass from SpecObjAll S where S.bestObjID ="+photo_objid
		query_result = sqlcl.query(sql_query).readlines()
		if len(query_result) > 1 :
			temp = string.split(query_result[1], ",")
			output_str = ""
			for x in temp:
				output_str = output_str + x.strip() + " "
			print output_str
		else :
			print "No spectrum found but photometric objid = ", photo_objid
		time.sleep(1.0)
	else :
		print "No object found"
else :
	sql_query = "select S.SpecObjID, S.plate, S.fiberID, S.mjd, S.z, S.zErr, S.specClass from SpecObjAll S where S.bestObjID ="+photo_objid
	query_result = sqlcl.query(sql_query).readlines()
	if len(query_result) > 1 :
		temp = string.split(query_result[1], ",")
		output_str = ""
		for x in temp:
			output_str = output_str + x.strip() + " "
		print output_str
	else :
		print "No spectrum found for the photometric objid = ", photo_objid
	time.sleep(1.0)
