#!/bin/bash

### Developed by Min-Su Shin 
### (Department of Astrophysical Sciences,
###  Princeton University)

ra=$1
dec=$2
seqid=$3
rad=120 # arcmin

wget "http://skydot.lanl.gov/nsvs/cone_search.php?ra=$ra&dec=$dec&rad=$rad&saturated=on&nocorr=on&lonpts=on&hiscat=on&hicorr=on&hisigcorr=on&radecflip=on" -O temp.txt >& /dev/null

awk -F'<th> Ngood    </th></tr>' '{print $2}' temp.txt | awk -F' ' '{if(NF > 2) print $0}' > temp.txt1
ex temp.txt1 << ends
%s/<\/tr>/\r/g
wq
ends

awk -F'</td><td>' '{print $1,$6}' temp.txt1 > temp.txt2
awk -F'</td><td align=right>' '{print $1,$2}' temp.txt2 > temp.txt3

ex temp.txt3 << ends
%s/<\/td>/ /g
%s/<\/a>/ /g
wq
ends

awk -F'>' '{print $5}' temp.txt3 > "$seqid".list
wc -l "$seqid".list

rm -f temp.txt*
