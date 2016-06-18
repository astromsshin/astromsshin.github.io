#!/usr/bin/env python

# Written by Min-Su Shin in Department of Astronomy, University of Michigan.
# Feel free use or revise the code.


import sys, httplib, string

wsid = 000000 # parameter : wsid of your account on CASJobs
pw = "00000" # parameter : password for your account on CASJobs

tb_name = sys.argv[1] # table name on your MyDB
fn = sys.argv[2] # upload file which has the first row whith column names. The file must be a CSV file.

print "# ", tb_name, fn

# Please, check the following web page for SOAP messages and relevant information
# http://casjobs.sdss.org/CasJobs/services/jobs.asmx?op=UploadData

SOAP_TEMPLATE = """
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <UploadData xmlns="http://Services.Cas.jhu.edu">
      <wsid>%d</wsid>
      <pw>%s</pw>
      <tableName>%s</tableName>
      <data>%s</data>
      <tableExists>%s</tableExists>
    </UploadData>
  </soap12:Body>
</soap12:Envelope>
"""

tb_data = ""
fd = open(fn, 'r')
cnt = 0
while 1:
	oneline = fd.readline()
	if not oneline: break
	tb_data = tb_data + oneline
	cnt = cnt + 1
fd.close()

SoapMessage = SOAP_TEMPLATE % (wsid, pw, tb_name, tb_data, "false") # parameter : false = overwriting the table on MyDB.

#construct and send the header
webservice = httplib.HTTP("casjobs.sdss.org")
webservice.putrequest("POST", "/CasJobs/services/jobs.asmx")
webservice.putheader("Host", "casjobs.sdss.org")
webservice.putheader("User-Agent", "Python post")
webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
webservice.putheader("Content-length", "%d" % len(SoapMessage))
webservice.endheaders()
webservice.send(SoapMessage)

# get the response
statuscode, statusmessage, header = webservice.getreply()
print "Response: ", statuscode, statusmessage
print "headers: ", header
res = webservice.getfile().read()
print res
