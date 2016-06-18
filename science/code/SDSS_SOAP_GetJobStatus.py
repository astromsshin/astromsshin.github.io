#!/usr/bin/env python

# Written by Min-Su Shin in Department of Astronomy, University of Michigan.
# Feel free use or revise the code.

import sys, urllib, string
import xml.dom.minidom

wsid = 000000 # parameter : wsid of your account on CASJobs
pw = "00000" # parameter : password for your account on CASJobs

# Please, check the following web page for SOAP messages and relevant information
# http://casjobs.sdss.org/CasJobs/services/jobs.asmx?op=GetJobStatus

jobid = sys.argv[1]

#construct and send
params = urllib.urlencode( {'wsid': wsid, 'pw':pw, 'jobId':jobid } )
f = urllib.urlopen("http://casjobs.sdss.org/CasJobs/services/jobs.asmx/GetJobStatus", params) # POST method
# get the response
dom = xml.dom.minidom.parse(f)
res = dom.getElementsByTagName("int")[0]
res_int = int(res.childNodes[0].data)
if res_int == 0:
	print "ready"
if res_int == 1:
	print "started"
if res_int == 2:
	print "canceling"
if res_int == 3:
	print "cancelled"
if res_int == 4:
	print "failed"
if res_int == 5:
	print "finished"
