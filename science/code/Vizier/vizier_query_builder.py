#!/usr/bin/env python

# Developed by Min-Su Shin
# (Department of Astrophysical Sciences, Princeton University)
# to query many objects to Simbad in a batch mode.

# This simple code generates a Vizier batch file.
# ./vizier_query_builder.py (list file) (query file)
# The generated file can be used with cdsclient package.


import sys
import string

# Vizquery file path
program_path="./cdsclient-3.2/vizquery"

# 2MASS
catalog_id="II/246"

position_fn = sys.argv[1]
position_fd = open(position_fn, 'r')
all_lines = position_fd.readlines()
position_fd.close()

out_fn = sys.argv[2]
out_fd = open(out_fn, 'w')

print position_fn, out_fn

out_fd.write(program_path+' -mime=csv -site=cfa << END\n')
out_fd.write('-source='+catalog_id+'\n')
out_fd.write('-c.eq=J2000\n')
out_fd.write('-c.rs=6.0\n')
#out_fd.write('-out=_q 2MASS Jmag Jcmsig Hmag Hcmsig Kmag Kcmsig _r prox\n')
out_fd.write('-out=_q 2MASS _r prox\n')
out_fd.write('-out.form=mini\n')
out_fd.write('-oc.form=dec\n')
out_fd.write('-c=<<====MyList\n')

for one_line in all_lines:
	temp = string.split(one_line)
	ra = temp[1]
	if float(temp[2]) < 0.0 :
		dec = temp[2]
	else :
		dec = "+"+temp[2]
	out_fd.write(ra+dec+'\n')

out_fd.write('====MyList\n')
out_fd.write('END\n')
out_fd.close()
