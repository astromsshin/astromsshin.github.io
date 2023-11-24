#!/usr/bin/env python

import sys, httplib, string

wsid = 
pw = 

tb_name = sys.argv[1]
fn = sys.argv[2]

print "# ", tb_name, fn


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

SoapMessage = SOAP_TEMPLATE % (wsid, pw, tb_name, tb_data, "false")

#construct and send the header
webservice = httplib.HTTP("skyserver.sdss3.org")
webservice.putrequest("POST", "/casjobs/services/jobs.asmx")
webservice.putheader("Host", "skyserver.sdss3.org")
webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
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
