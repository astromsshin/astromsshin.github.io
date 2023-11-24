#!/usr/bin/env python

# Written by Min-Su Shin, msshin (at) astro.princeton.edu (in 2005)
# msshin (at) umich.edu (in 2009), 
# Min-Su.Shin (at) astro.ox.ac.uk (in 2012), 
# msshin (at) kasi.re.kr (since 2015 - ).
# It needs the PhotoFlags.dat file.

import sys, commands, string

input_file = open("PhotoFlags.dat",'r')
flags=[]
hexcode=[]
while 1:
	line = input_file.readline()
	if not line : break
	lines = string.split(line)
	flags.append(lines[0])
	temp = float(lines[1])
	temp = int(temp)
	hexcode.append(hex(temp))
input_file.close()

result_hexcode = 0
result_flags = ""

for i in range(1, 33) :
	print "("+str(i)+")", flags[i-1]
selection1 = raw_input('Selection 1 => ')
lines = string.split(selection1)
for i in lines:
	result_hexcode = result_hexcode + int(float(hexcode[int(i)-1]))
	result_flags = result_flags + " " + flags[int(i)-1]

for i in range(33, 65) :
	print "("+str(i)+")", flags[i-1]
selection2 = raw_input('Selection 2 => ')
lines = string.split(selection2)
for i in lines:
	temp = string.split(hexcode[int(i)-1],'L')
	usednum = temp[0]
	result_hexcode = result_hexcode + int(float(usednum))
	result_flags = result_flags + " " + flags[int(i)-1]

result_hexcode= hex(result_hexcode)
result_hexcode = string.split(str(result_hexcode),'L')

print result_hexcode[0], result_flags
