#!/usr/bin/env python

# Written by Min-Su Shin (Princeton University)

import sys, commands, string

input_file = open("PrimTargetFlags.dat",'r')
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

for i in range(1, 31) :
	print "("+str(i)+")", flags[i-1]
selection1 = raw_input('Selection => ')
lines = string.split(selection1)
for i in lines:
	result_hexcode = result_hexcode + int(float(hexcode[int(i)-1]))
	result_flags = result_flags + " " + flags[int(i)-1]

result_hexcode= hex(result_hexcode)
result_hexcode = string.split(str(result_hexcode),'L')

print result_hexcode[0], result_flags
