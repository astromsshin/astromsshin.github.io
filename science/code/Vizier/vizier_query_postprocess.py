#!/usr/bin/env python

# Developed by Min-Su Shin
# (Department of Astrophysical Sciences, Princeton University)
# to query many objects to Vizier in a batch mode.

# This simple code process a Vizier result file.
# ./vizier_query_postprocess.py (list file) (result file) (output file)

import sys
import string

group_fn = sys.argv[1]
vizier_fn = sys.argv[2]
output_fn = sys.argv[3]

print group_fn, vizier_fn, output_fn

group_fd = open(group_fn, 'r')
all_lines_group = group_fd.readlines()
group_fd.close()
result_obj = dict()
result_distance = dict()
for objid in range(1, len(all_lines_group)+1):
	result_obj.setdefault(str(objid), 'NONE')
	result_distance.setdefault(str(objid), 'NONE')

vizier_fd = open(vizier_fn, 'r')
# reading headers
while 1:
	one_line = vizier_fd.readline()
	if one_line[0] == '-' : break

# reading main contents
cnt_line = 0
while 1:
	one_line = vizier_fd.readline()
	if not one_line: break
	if one_line == "\n": break # the result of Vizier has blanks
	parts = string.split(string.strip(one_line), ';')
	ind = int(parts[0]) - 1
	query_key = str(parts[0])
	obj_name = parts[1]
	distance = float(parts[2])
	return_obj = result_obj[query_key]
	if return_obj != 'NONE':
		return_distance = result_distance[query_key]
		if return_distance > distance:
			result_obj[query_key] = obj_name
			result_distance[query_key] = distance
	else :
		cnt_line = cnt_line + 1
		result_obj[query_key] = obj_name
		result_distance[query_key] = distance
print "# total number of matched objects = ",cnt_line,"/",len(all_lines_group)
vizier_fd.close()

output_fd = open(output_fn, 'w')
for objid in range(1, len(all_lines_group)+1):
	temp = str(objid)
	return_obj = result_obj[temp]
	return_distance = result_distance[temp]
	output_str = temp + " | " + return_obj + " | " + str(return_distance) + "\n"
	output_fd.write(output_str)
output_fd.close()
