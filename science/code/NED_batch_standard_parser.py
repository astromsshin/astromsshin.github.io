#!/usr/bin/env python

def print_usage():
	print """The NED batch parser parses output files from NED batch scripts. It works only 
for the "standard" output type!!! See http://nedwww.ipac.caltech.edu/help/batch.html"""
	print """If you have any questions and suggestions, feel free to contact Min-Su Shin (msshin @ kasi.re.kr)."""
	print "(Usage)"
	print "NED_batch_standard_parser.py [NED result file] [-o output filename]"
	print "-o : output filename. If it's not provided, standard output is default."
	print "It prints out IAU Name, type, distance from a search coordinate (arcmin), and redshift."
	print "(Example)"
	print "NED_batch_standard_parser.py 3arcsec.ned -o test.out"


import sys
import re
import string
import getopt

try:
	result_file = sys.argv[1]
	fd=open(result_file)
except:
	print_usage()
	sys.exit()

standard_output = 1
try:
	opts, args = getopt.getopt(sys.argv[2:], "o:v", ["output="])
	for o, a in opts:
		if o == "-o":
			standard_output = 0
			output_fn = a
except:
	standard_output = 1

print "Input file : ",result_file
lines = fd.readlines()
fd.close()

if standard_output < 1:
	out_fd = open(output_fn, 'w')
	print "Output file : ",output_fn

print "Parsing the result section..."
obj_cnt_yes_no = 0
obj_cnt = 0
for cnt in range(0,len(lines)):
	line = lines[cnt]
	return_val = re.findall('SEARCH RESULTS', line)
	if len(return_val) > 0:
		obj_cnt_yes_no = 1
	if obj_cnt_yes_no > 0:
		return_val = re.findall('NEARPOSN', line)
		if len(return_val) > 0:
			obj_cnt += 1
	return_val = re.findall('object\(s\) found', line)
	if len(return_val) > 0:
		output = []
		part = string.split(line)
		num_of_object = int(part[0])
		# choose the closest object
		result1 = lines[cnt+2]
		result2 = lines[cnt+5+num_of_object]
		result3 = lines[cnt+6+num_of_object]
		name = string.strip(result3[0:38])
		part = string.split(result1[26:])
		type = string.strip(part[0])
		distance = string.strip(part[3])
		part = string.split(result2[70:])
		if len(part) > 0 :
			redshift = part[0]
			try:
				dummy = int(redshift[0])
				if float(redshift) > 60.0 : # it prevents some weired results.
					redshift = "None"
			except:
				redshift = "None"
		else :
			redshift = "None"
		output.append(str(obj_cnt))
		output.append(name)
		output.append(type)
		output.append(distance)
		output.append(redshift)
		outstr = string.join(output, ',')
		if standard_output > 0:
			print outstr
		else:
			out_fd.write(outstr+"\n")

if standard_output < 1:
	out_fd.close()
