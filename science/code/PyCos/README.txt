PyCos - Python for Cosmology
developed by Min-Su Shin

It uses GNU Scientific Library for numerically intensive calculation. 
Therefore, the Python interface is generated from C++ source files by 
using the SWIG tool.

In short, the module can be used to calculate various kinds of distances, 
volumes, and age for given cosmological parameters. You can also get numbers 
about Schechter function quickly. It's a free software with the GPL license. 
But I'll be glad to hear any suggestions, applications, and bugs for the 
improved versions. The future version of this module will have more 
implementations. 

1. Install

First, change the setup.cfg file for your environment. You need to set 
directories of GNU Scientific Library.

Second, build the relevant libray and the Python interface by using
Swig. Simply, you need to type

python setup.py build

Third, install the module. Type 

python setup.py install

or

python setup.py install --prefix=(directory)

(NOTE) This module needs the GNU Scientific Library. Therefore, 
the library directory needed to be inclued in LD_LIBRAY_PATH.

2. Usage

The following is a simple test.

>>import PyCos
>>LCDM=PyCos.Cosmology()
>>dist=LCDM.ang_dist(3.0)
>>print dist
>>age_now=LCDM.age_now()
>>print age_now
>>LCDM=PyCos.Cosmology(0.3, 0.7, 0.0, -1.0, 0.70)
>>age=LCDM.age(2.0)
>>print age
>>conformal_time=LCDM.conformal_time(2.0)
>>print conformal_time
>>D_C=LCDM.D_C(2.0, 3.0)
>>print D_C

A complete explanation of all functions is given in
the doxygen documentation.
