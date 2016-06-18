#!/bin/bash

### Developed by Min-Su Shin 
### (Department of Astrophysical Sciences,
###  Princeton University)

rm -f all.htm
PREURL='<a href='
AFTERURL='>'
LASTURL='</a><br>'
for id in `cat count.list`
do
#	echo "Retrieving the basic information of $id"
	echo $id
	wget "http://skydot.lanl.gov/nsvs/star.php?num=$id&mask=32004" -O all.htm -o /dev/null
	ex all.htm << ends
	%s/</ /g
	%s/>/ /g
	w!
ends
	link=`awk -F' ' '{print $24}' all.htm | awk -F'"' '{print $2}'`
	link="http://skydot.lanl.gov/nsvs/"$link
#	echo $link
	wget "$link" -O $id.htm --user-agent="Python" -o /dev/null
	ex $id.htm << ends1
	%s/<tr>/MS/g
	%s/<td>/ /g
	%s/<\/td>/ /g
	w!
ends1
	awk -F'MS' '{print $2}' $id.htm | awk -F' ' '{print $1,$2,$3}' | awk -F' ' '{if(NF > 2) print $0}' > $id".web"
	rm -f $id".htm"
done
rm -f all.htm
