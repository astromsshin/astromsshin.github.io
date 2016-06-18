#!/usr/bin/env python

import math
import numpy
import pyfits
import scipy
import img_scale
from PIL import Image

# Parameters
red_fn = "frame-i-007907-6-0143.fits"
green_fn = "frame-r-007907-6-0143.fits"
blue_fn = "frame-g-007907-6-0143.fits"
sig_fract = 5.0
per_fract = 5.0-2
max_iter = 20
min_val = 0.0
red_non_linear_fact = 0.005
green_non_linear_fact = 0.005
blue_non_linear_fact = 0.005
saturation_parameter = 0.10


# Read red image
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
#sky, num_iter = img_scale.sky_median_sig_clip(img_data_r, sig_fract, per_fract, max_iter)
sky, num_iter = img_scale.sky_median_sig_clip(img_data_r, sig_fract, per_fract, max_iter, low_cut=False, high_cut=True)
print "sky = ", sky, "(", num_iter, ") for red image \
(", numpy.max(img_data_r), ",", numpy.min(img_data_r), ")"
img_data_r = img_data_r - sky


# Read green image
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
#sky, num_iter = img_scale.sky_median_sig_clip(img_data_g, sig_fract, per_fract, max_iter)
sky, num_iter = img_scale.sky_median_sig_clip(img_data_g, sig_fract, per_fract, max_iter, low_cut=False, high_cut=True)
print "sky = ", sky, "(", num_iter, ") for green image \
(", numpy.max(img_data_g), ",", numpy.min(img_data_g), ")"
img_data_g = img_data_g - sky


# Read blue image
hdulist = pyfits.open(blue_fn)
img_header = hdulist[0].header
img_data = hdulist[0].data
hdulist.close()
width=img_data.shape[0]
height=img_data.shape[1]
print "Blue file = ", blue_fn, "(", width, ",", height, ")"
img_data_b = numpy.array(img_data, dtype=float)
#sky = numpy.median(numpy.ravel(img_data_b))
#sky = numpy.mean(numpy.ravel(img_data_b))
#sky, num_iter = img_scale.sky_median_sig_clip(img_data_b, sig_fract, per_fract, max_iter)
sky, num_iter = img_scale.sky_median_sig_clip(img_data_b, sig_fract, per_fract, max_iter, low_cut=False, high_cut=True)
print "sky = ", sky, "(", num_iter, ") for blue image \
(", numpy.max(img_data_b), ",", numpy.min(img_data_b), ")"
img_data_b = img_data_b - sky


# Apply scaling relations
r = img_scale.asinh(img_data_r, scale_min = min_val, non_linear=red_non_linear_fact)
g = img_scale.asinh(img_data_g, scale_min = min_val, non_linear=green_non_linear_fact)
b = img_scale.asinh(img_data_b, scale_min = min_val, non_linear=blue_non_linear_fact)


# Estimate new scales for R, G, B
for y in range(r.shape[0]):
	for x in range(r.shape[1]):
		L_in = img_data_r[y][x] + img_data_g[y][x] + img_data_b[y][x]
		L_out = r[y][x] + g[y][x] + b[y][x]
		if L_in <= 0.0:
			L_in = 1.0e-4
			L_out = 0.0
		# R
		try:
			r[y][x] = math.pow(img_data_r[y][x] / L_in, saturation_parameter) * L_out
		except:
			r[y][x] = 0.0
		# G
		try:
			g[y][x] = math.pow(img_data_g[y][x] / L_in, saturation_parameter) * L_out
		except:
			g[y][x] = 0.0
		# B
		try:
			b[y][x] = math.pow(img_data_b[y][x] / L_in, saturation_parameter) * L_out
		except:
			b[y][x] = 0.0


# RGB image with SciPy
print "image size ", width, height
rgb_array = numpy.array( [numpy.ravel(scipy.misc.bytescale(r)), numpy.ravel(scipy.misc.bytescale(g)), numpy.ravel(scipy.misc.bytescale(b))] )
rgb_array = numpy.transpose(rgb_array)
rgb_array.astype(numpy.int)
PIL_data = []
for elm in rgb_array:
	PIL_data.append(tuple(elm))
use_image = Image.new('RGB', size=(height, width))
use_image.putdata(PIL_data)
use_image.save('rgb.png')
#use_image.show()
