#! /usr/bin/env python

"""
 Log file generator in HTML
 by Min-Su Shin (2009 -, University of Michigan)
                (2005 - 2009, Princeton University)
 Check the comments given in the code. You need to modify 
 the code for your own purposes, following the comments.
 You can also use this code to produce *multiple* files in different formats
 such as XML, TSV, and CSV.
"""


import string, fpformat, commands

num_per_page = 30 # the number of objects in a single page.

# The following two functions are provided here to 
# convert RA and DEC.
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


# Put your HTML header here. You also need to design your tables.
# In the following example, the table has seven columns.
html_header=""
html_header=html_header+"<html><title>Log</title><body>\n"
html_header=html_header+"<table border=1 align=center><tr><td>Field : ID</td><td>RA & DEC</td>\n"
html_header=html_header+"<td>Mag. +- Std.</td><td>Num.</td><td>FIRST ID</td><td>Fpeak Fint Rms</td><td>dist.</td></tr>\n"

# This file is read by the code.
# It is assumed that the file has multiple columns separated with blanks.
infn="FIRST.catalog.sort"
infp=open(infn,'r')
count=1
fcount=1 # the starting number of HTML pages.
while 1:
	oneline = infp.readline()
	if not oneline: break
	if (count % num_per_page == 1) and (count == 1):
		outfn="log_%d.htm" % (fcount) # Multiple HTML files are generated.
		outfp=open(outfn,'w')
		outfp.write(html_header)
		fcount = fcount + 1
	else:
		if (count % num_per_page == 1) and (count != 1):
			outfp.write("</table></html>") # this part writes the tail of HTML files and prepare the next file.
			outfp.close()
			outfn="log_%d.htm" % (fcount)
			outfp=open(outfn,'w')
			outfp.write(html_header)
			fcount = fcount + 1
	# It parses a single line of the input. The first column starts with an index 0.
	# If you want to use differnt separators, please, change the following line.
	# For example, if you want to use | as a separator, part=string.split(oneline, "|")
	part=string.split(oneline)
	# IMPORTANT: the following lines generate the HTML code which needs to be written to fill the table.
	# You should change the following lines for the format of your data.
	# Example of external links.
	lc_link="<a href=http://stardb.yonsei.ac.kr/lightcurve/nsvs_lightcurve_plot.php?id="+part[1]+" target=lc>"
	# Example of links to images stored in disks.
	out_str = "<tr><td><b>("+str(count)+")</b> "+part[0]+" : "+lc_link+part[1]+"</a><br><img src="+part[1]+".jpg></td>"
	# Example of converting angle units.
	ra_hms = deg2str_hms(float(part[2]))
	dec_dms = deg2str_dms(float(part[3]))
	# Example of external links to the Aladin service.
	out_str = out_str + "<td><a href=\"http://aladin.u-strasbg.fr/java/nph-aladin.pl?-script="+part[2]+" "+part[3]+"\" target=new>"+part[2]+" "+part[3]+"</a><br>"+ra_hms+" "+dec_dms+"</td>"
	out_str = out_str + "<td>"+part[4]+" +- "+part[5]+"</td>"
	out_str = out_str + "<td>"+part[6]+"</td>"
	out_str = out_str + "<td>"+part[7]+"</td>"
	out_str = out_str + "<td>"+part[8]+" "+part[9]+" "+part[10]+"</td>"
	out_str = out_str + "<td>"+part[11]+"</td></tr>"
	out_str = out_str+"\n"
	# IMPORTANT: the table row is written here.
	outfp.write(out_str)
	count = count + 1 # this count is used to trace how many objects have been written in a single HTML file.
outfp.write("</table></html>")
outfp.close()
