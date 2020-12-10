#!/usr/bin/env python3

# Presented by Min-Su Shin 
# (2015 - , KASI, Republic of Korea)
# (2012 - 2015; Astrophysics, University of Oxford).

# This is an example code which converts astronomical fits images to 
# an OpenEXR file (http://www.openexr.com/). This file format supports 
# 32-bit floating-point which is commonly used in astronomical FITS files.
# OpenEXR is one common format for a high dynamic-range (HDR) image.

# Here, I use astropy, numpy, and Python OpenEXR binding.
# conda install openexr-python numpy astropy
# You may find pfstools (http://pfstools.sourceforge.net/) and 
# exrtools (http://scanline.ca/exrtools/) useful in order to 
# check the output EXR files.

from astropy.io import fits

# read FITS images
# red channel
fits_fn = "i.fits"
hdulist = fits.open(fits_fn)
r_img_header = hdulist[0].header
r_img_data = hdulist[0].data
hdulist.close()
width=r_img_data.shape[0]
height=r_img_data.shape[1]
print("reading the FITS file ",fits_fn," done...")
print(r_img_data.dtype)
# green channel
fits_fn = "r.fits"
hdulist = fits.open(fits_fn)
g_img_header = hdulist[0].header
g_img_data = hdulist[0].data
hdulist.close()
width=g_img_data.shape[0]
height=g_img_data.shape[1]
print("reading the FITS file ",fits_fn," done...")
print(g_img_data.dtype)
# blue channel
fits_fn = "g.fits"
hdulist = fits.open(fits_fn)
b_img_header = hdulist[0].header
b_img_data = hdulist[0].data
hdulist.close()
width=b_img_data.shape[0]
height=b_img_data.shape[1]
print("reading the FITS file ",fits_fn," done...")
print(b_img_data.dtype)

# write an EXR file
import OpenEXR
import numpy
exr_fn = "galaxy.exr"
r_img_data = numpy.asarray(r_img_data, dtype=numpy.float32)
r_img_data = r_img_data.tobytes()
g_img_data = numpy.asarray(g_img_data, dtype=numpy.float32)
g_img_data = g_img_data.tobytes()
b_img_data = numpy.asarray(b_img_data, dtype=numpy.float32)
b_img_data = b_img_data.tobytes()
out_exr = OpenEXR.OutputFile(exr_fn, OpenEXR.Header(width, height))
out_exr.writePixels({'R': r_img_data, 'G': g_img_data, 'B': b_img_data})
print("write the EXR file ",exr_fn," done...")
