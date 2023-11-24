#!/usr/bin/env python

import numpy
import pyfits
import img_scale
import pylab
import math


# Parameters
blue_fn = "g.fits"
green_fn = "r.fits"
red_fn = "i.fits"
sig_fract = 3.0
per_fract = 5.0-4
max_iter = 50
min_val = 0.0
non_linear_fact = 0.005
out_fn = "rgb.png"
axis_tag = False
#axis_tag = True


# Blue image
hdulist = pyfits.open(blue_fn)
img_header = hdulist[0].header
img_data = hdulist[0].data
hdulist.close()
width=img_data.shape[0]
height=img_data.shape[1]
print "Blue file = ", blue_fn, "(", width, ",", height, ")"
img_data_b = numpy.array(img_data, dtype=float)
rgb_array = numpy.empty((width,height,3), dtype=float)
#sky = numpy.median(numpy.ravel(img_data_b))
#sky = numpy.mean(numpy.ravel(img_data_b))
sky, num_iter = img_scale.sky_median_sig_clip(img_data_b, sig_fract, per_fract, max_iter)
print "sky = ", sky, "(", num_iter, ") for blue image \
(", numpy.max(img_data_b), ",", numpy.min(img_data_b), ")"
img_data_b = img_data_b - sky
b = img_scale.asinh(img_data_b, scale_min = min_val, non_linear=non_linear_fact)

# Green image
hdulist = pyfits.open(green_fn)
img_header = hdulist[0].header
img_data = hdulist[0].data
hdulist.close()
width=img_data.shape[0]
height=img_data.shape[1]
print "Green file = ", green_fn, "(", width, ",", height, ")"
img_data_g = numpy.array(img_data, dtype=float)
#sky = numpy.median(numpy.ravel(img_data_g))
#sky = numpy.mean(numpy.ravel(img_data_g))
sky, num_iter = img_scale.sky_median_sig_clip(img_data_g, sig_fract, per_fract, max_iter)
print "sky = ", sky, "(", num_iter, ") for green image \
(", numpy.max(img_data_g), ",", numpy.min(img_data_g), ")"
img_data_g = img_data_g - sky
g = img_scale.asinh(img_data_g, scale_min = min_val, non_linear=non_linear_fact)

# Red image
hdulist = pyfits.open(red_fn)
img_header = hdulist[0].header
img_data = hdulist[0].data
hdulist.close()
width=img_data.shape[0]
height=img_data.shape[1]
print "Red file = ", red_fn, "(", width, ",", height, ")"
img_data_r = numpy.array(img_data, dtype=float)
#sky = numpy.median(numpy.ravel(img_data_r))
#sky = numpy.mean(numpy.ravel(img_data_r))
sky, num_iter = img_scale.sky_median_sig_clip(img_data_r, sig_fract, per_fract, max_iter)
print "sky = ", sky, "(", num_iter, ") for red image \
(", numpy.max(img_data_r), ",", numpy.min(img_data_r), ")"
img_data_r = img_data_r - sky
r = img_scale.asinh(img_data_r, scale_min = min_val, non_linear=non_linear_fact)


# RGB image with Matplotlib
rgb_array[:,:,0] = r
rgb_array[:,:,1] = g
rgb_array[:,:,2] = b
print "Plotting a RGB image of (", width,",",height,")"
pylab.imshow(rgb_array, interpolation='nearest', origin='lower')
if axis_tag != True:
	pylab.axis('off')
pylab.savefig(out_fn)
