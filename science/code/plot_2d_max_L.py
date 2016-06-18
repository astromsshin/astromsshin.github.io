#!/usr/bin/env python

import string
import math
# package : numpy
import numpy
# package : matplotlib
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches

# reading files
infn = "lowz.mass.density.non_broad"
infp = open(infn, 'r')
var1_list = [] # mass
var2_list = [] # density
n_data = 0
while 1:
	oneline = infp.readline()
	if not oneline: break
	n_data = n_data + 1
	parts = string.split(oneline)
	mass = math.log10(float(parts[6])) # column 7 = var1
	density = math.log10(float(parts[5])) # column 6 = var2
	var1_list.append(mass)
	var2_list.append(density)
infp.close()

# checking the data
max_var1 = max(var1_list)
min_var1 = min(var1_list)
max_var2 = max(var2_list)
min_var2 = min(var2_list)

# parameters that require optimization
var1_min = 8.9
var1_max = 11.8
var2_min = -6.03
var2_max = 0.11
n1_min = 5
n1_max = 50
n2_min = 5
n2_max = 50
delta_factor = 0.0
alpha_factor = 1.0
if (max_var1 > var1_max) :
	print "# WARNING : MAX_VAR1 %g > VAR1_MAX %g" % (max_var1, var1_max)
if (min_var1 < var1_min) :
	print "# WARNING : MIN_VAR1 %g < VAR1_MIN %g" % (min_var1, var1_min)
if (max_var2 > var2_max) :
	print "# WARNING : MAX_VAR2 %g > VAR2_MAX %g" % (max_var2, var2_max)
if (min_var2 < var2_min) :
	print "# WARNING : MIN_VAR2 %g < VAR2_MIN %g" % (min_var2, var2_min)

# likelihood
n1_list = range(n1_min, n1_max+1)
n2_list = range(n2_min, n2_max+1)
L_dist = numpy.zeros((n1_max - n1_min + 1, n2_max - n2_min + 1))
for loop1 in range(n1_min, n1_max+1):
	delta1 = (var1_max - var1_min)/float(loop1)
	for loop2 in range(n2_min, n2_max+1):
		delta2 = (var2_max - var2_min)/float(loop2)
		# space to store N_i,j
		N = numpy.zeros((loop1,loop2), dtype=numpy.int)
		for ind in range(0, n_data):
			x = var1_list[ind]
			y = var2_list[ind]
			i = math.floor((x - var1_min)/delta1 - delta_factor)
			j = math.floor((y - var2_min)/delta2 - delta_factor)
			N[i,j] = N[i,j] + 1
		# likelihood for this binning
		div_factor = (n_data + alpha_factor*loop1*loop2 - 1.0) \
		* delta1 * delta2
		L = 0.0
		for ind1 in range(0, loop1):
			for ind2 in range(0, loop2):
				temp = (N[ind1,ind2] + alpha_factor - 1.0)/div_factor
				if temp > 0 :
					temp = math.log(temp)
				else :
					temp = 0.0
				L = L + N[ind1,ind2]*temp
#		print loop1, loop2, L
		L_dist[loop1 - n1_min, loop2 - n2_min] = L

# result
solution = L_dist.argmax()
n1_best = int(math.floor(solution / (n1_max - n1_min + 1)))
n2_best = solution % (n1_max - n1_min + 1)
#print n1_best, n2_best
L_found = L_dist[n1_best, n2_best]
#L_correct = L_dist.max()
#print L_found, L_correct
n1_best = n1_list[n1_best]
n2_best = n2_list[n2_best]
print "##### Results #####"
print "(n1, n2) = %d, %d" % (n1_best, n2_best)
print "###################"

	
# plot
pyplot.figure()
cnt_list = [0.75, 0.50, 0.25, 0.1, 0.02]
for ind in range(0, len(cnt_list)):
	cnt_list[ind] = L_correct * cnt_list[ind]
#pyplot.contour(n1_list, n2_list, L_dist)
pyplot.contour(n1_list, n2_list, L_dist, 10)
pyplot.grid(linestyle=':')
#pyplot.contour(n1_list, n2_list, L_dist, cnt_list)
outstr = "(%d, %d)" % (n1_best, n2_best)
pyplot.text(n1_best, n2_best, outstr, horizontalalignment='center', verticalalignment='center')
pyplot.xlabel("# of bins (variable 1)")
pyplot.ylabel("# of bins (variable 2)")
pyplot.title('Likeliehood  distribution')
pyplot.savefig('plot.png')

