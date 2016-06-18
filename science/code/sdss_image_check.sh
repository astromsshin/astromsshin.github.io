#!/bin/bash

# arg 1 = ra (deg) arg 2 = dec (deg)

if [ $# != '2' ]; then
        echo "usage : sdss_image_check.sh ra(deg) dec(deg)"
        exit 0
fi

wget -q "http://das.sdss.org/DR7-cgi-bin/FOOT?Submit=Submit%20Request;csvIn=ra%2Cdec%0D%0A"$1"%2C"$2"%0D%0A%0D%0A;inputFile=;do_bestBox=yes" -O ./$$.result
check_result=`grep "0,    0,    0,    0,     0,      0" $$".result" | wc -l`
if [ "$check_result" -eq "0" ] 
then
	echo "YES"
else
	echo "NO"
fi
rm -f ./$$.result
