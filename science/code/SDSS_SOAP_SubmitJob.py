#!/usr/bin/env python

# Written by Min-Su Shin in Department of Astronomy, University of Michigan.
# Feel free use or revise the code.

import sys, urllib, string
import xml.dom.minidom

wsid = 000000 # parameter : wsid of your account on CASJobs
pw = "00000" # parameter : password for your account on CASJobs

tb_name = sys.argv[1]

print "# ", tb_name

# 6 arcsec search
sql_query = """
CREATE TABLE %s (
nsvs_id int not null,
objid bigint not null,
distance float not null,
type int not null,
psfMag_u real not null,
psfMagErr_u real not null,
flags_u bigint not null,
psfMag_g real not null,
psfMagErr_g real not null,
flags_g bigint not null,
psfMag_r real not null,
psfMagErr_r real not null,
flags_r bigint not null,
psfMag_i real not null,
psfMagErr_i real not null,
flags_i bigint not null,
psfMag_z real not null,
psfMagErr_z real not null,
flags_z bigint not null,
specObjID bigint not null
)
""" % (tb_name)


# Please, check the following web page for SOAP messages and relevant information
# http://casjobs.sdss.org/CasJobs/services/jobs.asmx?op=SubmitJob

# parameter : a default context is DR7
# parameter : taskname
# parameter : estimate of execution time (min)

params = urllib.urlencode( {'wsid': wsid, 'pw':pw, 'qry': sql_query, 'context': "DR7", 'taskname': tb_name, 'estimate': 30} )
f = urllib.urlopen("http://casjobs.sdss.org/CasJobs/services/jobs.asmx/SubmitJob", params) # POST method
# get the response
dom = xml.dom.minidom.parse(f)
job_id = dom.getElementsByTagName("long")[0]
job_id_str = job_id.childNodes[0].data
print job_id_str # job id
