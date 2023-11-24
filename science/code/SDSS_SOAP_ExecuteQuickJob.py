#!/usr/bin/env python

# Written by Min-Su Shin in Department of Astronomy, University of Michigan.
# Feel free use or revise the code.

import sys, httplib, string

wsid = 000000 # parameter : wsid of your account on CASJobs
pw = "00000" # parameter : password for your account on CASJobs

tb_name = sys.argv[1]

print "# ", tb_name

# Please, check the following web page for SOAP messages and relevant information
# http://casjobs.sdss.org/CasJobs/services/jobs.asmx?op=ExecuteQuickJob

SOAP_TEMPLATE = """
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <ExecuteQuickJob xmlns="http://Services.Cas.jhu.edu">
      <wsid>%d</wsid>
      <pw>%s</pw>
      <qry>%s</qry>
      <context>%s</context>
      <taskname>%s</taskname>
      <isSystem>%s</isSystem>
    </ExecuteQuickJob>
  </soap12:Body>
</soap12:Envelope>
"""

# the following example creates a new table "tb_name".
sql_query = """
CREATE TABLE %s (
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


SoapMessage = SOAP_TEMPLATE % (wsid, pw, sql_query, "MyDB", tb_name, "true")
# MyDB is the context of the example query.

#construct and send the header
webservice = httplib.HTTP("casjobs.sdss.org")
webservice.putrequest("POST", "/CasJobs/services/jobs.asmx")
webservice.putheader("Host", "casjobs.sdss.org")
webservice.putheader("User-Agent", "Python post")
webservice.putheader("Content-type", "application/soap+xml; charset=\"UTF-8\"")
webservice.putheader("Content-length", "%d" % len(SoapMessage))
webservice.endheaders()
webservice.send(SoapMessage)

print "# %d\n" % (len(SoapMessage))

# get the response
statuscode, statusmessage, header = webservice.getreply()
print "Response: ", statuscode, statusmessage
print "headers: ", header
res = webservice.getfile().read()
print res
