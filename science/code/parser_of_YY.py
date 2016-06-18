#!/bin/env python

# Parsing Yonsei-Yale Isochrone by age
# Written by Min-Su Shin (astroshin@yonsei.ac.kr), Department of Astronomy, Yonsei University

import string, sys

if(len(sys.argv) != 2) :
	print "Usage: Parser_of_YY.py [YY isochrone file name]"
	sys.exit()

fn_for_input = sys.argv[1]
input_file = open(fn_for_input, 'r')
# Reading two lines of explanation
line_one = input_file.readline()
line_one = input_file.readline()
open_check = '0'
while 1:
	line_one = input_file.readline()
	if not line_one : 
		print "Completed!!!"
		input_file.close()
		output_file.close()
		break
	if line_one[0] == 'a':
		if open_check == '0':
			data_array = string.split(line_one,'=')
			temp_name = string.split(data_array[1])
			age = temp_name[0]
			print "Processing : Age ",age
			new_fn = fn_for_input + '.age' + age
			output_file = open(new_fn, 'w')
			open_check = '1'
		else :
			output_file.close()
			data_array = string.split(line_one,'=')
			temp_name = string.split(data_array[1])
			age = temp_name[0]
			print "Processing : Age ",age
			new_fn = fn_for_input + '.age' + age
			output_file = open(new_fn, 'w')
			open_check = '1'
	# Skip of the gap
	elif line_one[1] == '\n':
		pass
	elif line_one:
		output_file.write(line_one)
	else:
		pass
