#!/usr/bin/env python

import numpy
import pyfits
import img_scale
import pylab

fn = "frame-r-007907-6-0143.fits"
sig_fract = 5.0
percent_fract = 0.01

hdulist = pyfits.open(fn)
img_header = hdulist[0].header
img_data_raw = hdulist[0].data
hdulist.close()
width=img_data_raw.shape[0]
height=img_data_raw.shape[1]
print "#INFO : ", fn, width, height
img_data_raw = numpy.array(img_data_raw, dtype=float)
#sky, num_iter = img_scale.sky_median_sig_clip(img_data, sig_fract, percent_fract, max_iter=100)
sky, num_iter = img_scale.sky_mean_sig_clip(img_data_raw, sig_fract, percent_fract, max_iter=10)
print "sky = ", sky, '(', num_iter, ')'
img_data = img_data_raw - sky
min_val = 0.0
print "... min. and max. value : ", numpy.min(img_data), numpy.max(img_data)

new_img = img_scale.sqrt(img_data, scale_min = min_val)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('sqrt.png')
pylab.clf()
new_img = img_scale.power(img_data, power_index=3.0, scale_min = min_val)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('power.png')
pylab.clf()
new_img = img_scale.log(img_data, scale_min = min_val)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('log.png')
pylab.clf()
new_img = img_scale.linear(img_data, scale_min = min_val)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('linear.png')
pylab.clf()
new_img = img_scale.asinh(img_data, scale_min = min_val, non_linear=0.01)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('asinh_beta_01.png')
pylab.clf()
new_img = img_scale.asinh(img_data, scale_min = min_val, non_linear=0.5)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('asinh_beta_05.png')
pylab.clf()
new_img = img_scale.asinh(img_data, scale_min = min_val, non_linear=2.0)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('asinh_beta_20.png')
pylab.clf()
new_img = img_scale.histeq(img_data_raw, num_bins=256)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('histeq.png')
pylab.clf()
new_img = img_scale.logistic(img_data_raw, center = 0.03, slope = 0.3)
pylab.imshow(new_img, interpolation='nearest', origin='lower', cmap=pylab.cm.hot)
pylab.axis('off')
pylab.savefig('logistic.png')
pylab.clf()
