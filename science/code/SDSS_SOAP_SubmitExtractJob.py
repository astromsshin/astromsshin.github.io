#!/usr/bin/env python

# Written by Min-Su Shin in Department of Astronomy, University of Michigan.
# Feel free use or revise the code.

import sys, httplib, string
import xml.dom.minidom

wsid = 000000 # parameter : wsid of your account on CASJobs
pw = "00000" # parameter : password for your account on CASJobs

# Please, check the following web page for SOAP messages and relevant information
# http://casjobs.sdss.org/CasJobs/services/jobs.asmx?op=SubmitExtractJob

tb_name = sys.argv[1]
print "# ", tb_name


SOAP_TEMPLATE = """
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <SubmitExtractJob xmlns="http://Services.Cas.jhu.edu">
      <wsid>%d</wsid>
      <pw>%s</pw>
      <tableName>%s</tableName>
      <type>%s</type>
    </SubmitExtractJob>
  </soap12:Body>
</soap12:Envelope>
"""

SoapMessage = SOAP_TEMPLATE % (wsid, pw, tb_name, "CSV") # parameter : CSV format

#construct and send the header
webservice = httplib.HTTP("casjobs.sdss.org")
webservice.putrequest("POST", "/CasJobs/services/jobs.asmx")
webservice.putheader("Host", "casjobs.sdss.org")
webservice.putheader("User-Agent", "Python post")
webservice.putheader("Content-type", "application/soap+xml; charset=\"UTF-8\"")
webservice.putheader("Content-length", "%d" % len(SoapMessage))
webservice.endheaders()
webservice.send(SoapMessage)

#print "# %d\n" % (len(SoapMessage))

# get the response
statuscode, statusmessage, header = webservice.getreply()
#print "Response: ", statuscode, statusmessage
#print "headers: ", header
res = webservice.getfile().read()
dom = xml.dom.minidom.parseString(res)
res = dom.getElementsByTagName("SubmitExtractJobResult")[0]
res_int = int(res.childNodes[0].data)
print res_int
