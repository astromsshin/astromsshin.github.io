#!/usr/bin/env python

# Develeoped by Min-Su Shin
#               (Princeton University 2005-2009)
#               (University of Michigan 2009-2012)
#               (University of Oxford 2012- )

import getopt, sys
import time
import urllib
import string
from xml.dom import minidom

url_IRSA='http://irsa.ipac.caltech.edu/cgi-bin/FinderChart/nph-finder'

# objname='SDSSJ001027.3-104341'
# ra="2.6141316" # deg
# dec="-10.728253" # deg
# size="4.0" # arcmin


def single_download(objname, ra, dec, size):
  coord=ra+" "+dec
  ###### default parameters ######
  # the following is the default parameter for my own work.
  # You can find explanations of the options on the IRSA web page
  # http://irsa.ipac.caltech.edu/applications/FinderChart/docs/finderProgramInterface.html
  # In short, if you want to get 2MASS only images, set "survey": "2MASS".
  # But when you need 2MASS and SDSS together, simply add "survey":"2MASS" in to
  # the following tupule.
  # WARN: as explained on the IRSA web page, DSS and SDSS images are not stored
  # on the IRSA system. Therefore, the elapsed time for those images can vary 
  # due to the system status.
  ################################
  parameters={"mode": "prog", "locstr": coord, "subsetsize": size, \
  "survey": "SDSS", "orientation": "left", "reproject": "false", "grid_orig": "false", \
  "grid_shrunk": "false", "markervis_orig": "true", "markervis_shrunk": "true"}
  # connection to IRSA
  print "# Retrieving image information from IRSA"
  t1 = time.time()
  url_data = urllib.urlencode(parameters)
  res = urllib.urlopen(url_IRSA, url_data)
  t2 = time.time()
  print "... %f seconds" % (t2 - t1)
  # extraction of XML data
  use_dom = minidom.parse(res)
  temp = use_dom.getElementsByTagName('finderchart')
  temp = temp[0]
  status_value = temp.attributes["status"].value
  if status_value != "ok":
    print "... failed with finderchart status=",status_value
    return 1
  temp = use_dom.getElementsByTagName('totalimages')
  temp = temp[0]
  number_of_images = int(temp.firstChild.data)
  print "# the number of images = %d " % (number_of_images)
  i = 1
  for image_node in use_dom.getElementsByTagName('image'):
    str_ind = "%02d" % (i)
    survey = image_node.getElementsByTagName('surveyname')
    survey = survey[0].firstChild.data
    survey = survey.strip()
    band = image_node.getElementsByTagName('band')
    band = band[0].firstChild.data
    band = band.strip()
    # FITS files
    fits_url = image_node.getElementsByTagName('fitsurl')
    fits_url = fits_url[0].firstChild.data
    fits_url = fits_url.strip()
    out_fn_fits = objname+"_"+str_ind+"_"+survey+"_"+band+".fits"
#    print "..."+fits_url
    print "..."+out_fn_fits
    urllib.urlcleanup()
    t1 = time.time()
    urllib.urlretrieve(fits_url, out_fn_fits)
    t2 = time.time()
    print "... %f seconds" % (t2 - t1)
    # Shrunk JPEG files
    small_jpeg_url = image_node.getElementsByTagName('shrunkjpgurl')
    small_jpeg_url = small_jpeg_url[0].firstChild.data
    small_jpeg_url = small_jpeg_url.strip()
    out_fn_small_jpeg = objname+"_"+str_ind+"_"+survey+"_"+band+"_small.jpg"
#    print "..."+small_jpeg_url
    print "..."+out_fn_small_jpeg
    urllib.urlcleanup()
    t1 = time.time()
    urllib.urlretrieve(small_jpeg_url, out_fn_small_jpeg)
    t2 = time.time()
    print "... %f seconds" % (t2 - t1)
    # JPEG files
    jpeg_url = image_node.getElementsByTagName('jpgurl')
    jpeg_url = jpeg_url[0].firstChild.data
    jpeg_url = jpeg_url.strip()
    out_fn_jpeg = objname+"_"+str_ind+"_"+survey+"_"+band+".jpg"
#    print "..."+jpeg_url
    print "..."+out_fn_jpeg
    urllib.urlcleanup()
    t1 = time.time()
    urllib.urlretrieve(jpeg_url, out_fn_jpeg)
    t2 = time.time()
    print "... %f seconds" % (t2 - t1)
    i = i + 1


infn="obj.list"
infp=open(infn, 'r')
while 1:
  oneline = infp.readline()
  if not oneline: break
  parts = string.split(oneline)
  objname = parts[0]
  ra = parts[1]
  dec = parts[2]
  size = "4.0" # arcmin
  single_download(objname, ra, dec, size)
infp.close()
