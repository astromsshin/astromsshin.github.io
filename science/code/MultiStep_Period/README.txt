MS_Period (Multi-Step Period; a.k.a., Min-Su Shin Period)
: programs to determine periods of variable stars. 

 - Made by Min-Su Shin ( Sep., 2002 - )
   If you have problems with the code, let me know the problems. I will 
   be able to help you figure out the problems. The main reference is 
   Shin & Byun, JKAS, 37, 79 (2004).

 - References : MNRAS, 241, 153-165 (1989)
		ApJ, 436, 787-794 (1994)
		ApJ, 460, L107-L110 (1996)
		ApJ, 489, 941-945 (1997)
		ApJ, 516, 315-323 (1999)
		JKAS, 37, 79-85 (2004)

 - Note : minmax.c is from Eric Weeks 
          ( http://www.physics.emory.edu/~weeks/software/minmax.c ).
          The minmax.c is included in this program with his permission.

 - Acknowledgments: A. Schwarzenberg-Czerny, Carl W. Akerlof, and 
                    Eric Weeks.

**************************************************************************************************** 

 [ IMPORTANT!!! ]
 Before compiling the codes, you have to patch minmax.c.
 patch minmax.c < minmax.patch
 Depending on the size of periodogram files, i.e. the range of trial periods and 
 the step size of trial periods, you have to change the parameter MAX_PTR_NUM 
 in minmax.c file.

 [ IMPORTANT!!! ]
 This version supporting OpenMP can be used without OpenMP. Check the Makefile.
 OMP_NUM_THREADS environment variable controls the number of threads used by the code.

 [ IMPORTANT!!! ]
 Tests on MacOS showed that some compilers do not work for a standard C library 
 function "modf" somewhere in the code. Because of this issue, I used a standard 
 C library function "fmod" with some tricks.

 [ IMPORTANT!!! ]
 Users can change important parameters which are set by C macros found in common.h. 
 First, USE_NBIN determines how many bins in phase space should be used to estimate 
 ANOVA statistic. Second, USE_DEGREE controls the degree of multiple-harmonics terms. 
 Third, DEFAULT_dP_over_P works as a default value to set the step size of trial 
 periods for phase and multi.

 [ IMPORTANT!!! ]
 The second step conducted by spline uses an important value set by C macro 
 DEFAULT_dP_plus_P_over_P found in spline.c. This determines the step size 
 of trial periods in the second step.

 [ IMPORTANT!!! ]
 Check period.sh and its options. period.sh is a simple shell script to make 
 the two-step procedure convenient. However, you can use multi, phase, and spline 
 independently.

 [ IMPORTANT!!! : check Makefile ]
 In order to compile all programs, you should check Makefile. In particular, first, 
 compile the code without optimization which sometimes causes problems. And then 
 test the compiled code. If it works, you can try to compile the code with optimization.
 The Makefile can compile the following:

 1) multi - Multiharmonic function fitting without using weighting factors.
            Multiharmonic function fitting with using weighting factors. (USE_ERR macro).
            Multiharmonic function fitting with resampling estimation. (USE_RESAMPLE macro).

 2) phase - Phase folding without using weighting factors.
            Phase folding with using weighting factors. (USE_ERR macro).
            Phase folding with resampling estimation. (USE_RESAMPLE macro).

 For multi and phase, you can compbine three macros (_OPENMP, USE_ERR, USE_RESAMPLE) together.

 3) spline - Least square cubic spline fitting.

 4) fold - Folding time series date in order to make a light curve.

 5) minmax - Finding local maximum points in the periodograms.

-----------------------------------------------------------------------------------------------------

 There are four shell scripts:

 1) period.sh - Its products are candidate periods.
    (Usage) period.sh 184010-0047
    where '184010-0047' is a sorted time series data file with three columns: date, mag., and mag. error

 2) periodogram_plot.sh - It uses SM to plot periodograms.
    (Usage) periodogram_plot.sh 184010-0047.multi.summary

 3) light_curve_fold.sh - It uses SM to draw a light curve
    with a given period.
    (Usage) light_curve_fold.sh 184010-0047 0.435801

 4) light_curve_raw.sh - It uses SM to draw a light curve.
    (Usage) light_curve_raw.sh 184010-0047

----------------------------------------------------------------------------------------------------

 Additional Python scripts:

 1) candidate.py - It is used to make a file which have candidate periods. This is also a key 
                   script to run the second step of using the Spline fitting in the multi-step
                   period search.

 2) spline.py - Supplementary Python script to run spline independently.
                In the source code, range_factor constrols the range of periods searched
                around the given trial period.
    (usage) ./spline.py data_use.txt 163 0.593350 data_use.txt.spline.pdg

 3) save_pdg.py - It is used by period.sh to save parts of periodograms.

 4) read_plot_sample.py - It can be used to read/plot periodograms and light curves.

 5) read_plot_resample.py - It can be used to read/plot periodogram estimation and 
                            partial estimation by the resampling method.

 test_plot.py shows how you can use read_plot_sample.py and read_plot_resample.py to 
 read/plot files generated by MS_Period.

----------------------------------------------------------------------------------------------------

 [ NOTE ]
- GNU Scientific library Ver. 1.3 (GSL V. 1.3) is used for multi.c and phase.c files 
 when USE_ERR found in common.h is on. Higher versions will work too.
- SM(super mongo) is in the plotting shell scripts.
- If you want to use Python scripts to read/plot the output files, you need 
 to have NumPy and Matplotlib.
- Some Linux/Unix commands such as sort and wc are needed in the programs.

*********** Sample Data *******************

 184010-0047 : the observation data from ASAS project.
 184010-0047.fold.model : the fitted model light curve in the phase space.

 ./period.sh 184010-0047 should show the following result.

 For debugging purpose, you can change a shell variable DEBUGE_MODE 
 in period.sh. The following is the example output from perio.sh 
 when using 8 threads.

# Multi-Step Period (MS-Period) : tool made by Min-Su Shin
[log] FACTOR_MIN_MAX_PERIOD=0
[log] MIN_PERIOD_FACTOR=1.0
[log] MAX_PERIOD_FACTOR=1.0
[log] CUT_MIN_MAX_PERIOD=0
[log] MIN_PERIOD=0.10
[log] MAX_PERIOD=0.50
[log] STORE_PDG=1
[log] STORE_TOP_PEAK=1
[log] STORE_PEAK_NUMBER=30
[log] STORE_NUMBER=10
[log] STORE_FACTOR=0.001
[log] STORE_CHI2=1
[log] NUM_CANDIDATE=-1
[log] SPLINE_RANGE_CHANGE=0
[log] SPLINE_RANGE_FACTOR=0.0005
[log] SPLINE_STEP_SIZE_CHANGE=0
[log] SPLINE_STEP_SIZE=0.00001
# 816  data points in the file 184010-0047
# 1 - 1. Starting Function Fitting Algorithm
# OpenMP is working with 8 CPUs
# Min f. 0.014511 Max f. 473.845046 Min P. 0.013260 Max P. 432.979850
# 1 - 2. Starting Phase Folding Algorithm
# OpenMP is working with 8 CPUs
# Min f. 0.014511 Max f. 473.845046 Min P. 0.013260 Max P. 432.979850
# ... save the parts of periodograms
# ... save +- 10 points 
# ... the fraction 0.0605827 approximately 
# ... save +- 10 points 
# ... the fraction 0.0605827 approximately 
# 2. Spline fitting for the candidate periods
# RESULT : initially estimated period, final period, and reduced chi^2
# Result from multi-harmonic function method
 0.435675 0.435801 2952.641130
 0.653730 0.653691 31069.096362
 0.871791 0.871599 2915.028393
 0.217945 0.217882 33392.484607
 1.089461 1.089548 31407.280752
# Result from phase-dispersion minimization
 0.278696 0.278771 51033.443076
 0.178813 0.178845 53306.537858
 0.557673 0.557461 56894.389650
 0.774029 0.773743 65129.393185
 0.303408 0.303335 61345.813010

*********** FAQ ***********

1. How does this multi-step period finding work?
: candidate periods are chosen by two methods: phase dispersion minimization and 
multi-harmonic function fitting. When the number of candidate periods is 10, 
top five best candidate periods are selected by the multi-harmonic function fitting. 
The rest five candidates are found by the phase dispersion minimization, 
avoiding the same candidates which are already selected by the multi-harmonic function 
fitting. These candidate periods are used by the Spline fitting method which find the best 
"refined" period with the smallest chi^2 around the candidate periods.

2. Does the refined period with the smallest chi^2 value represent the best 
estimation of a correct period?
: it's dangerous to adopt the period with the smallest chi^2 value as the best estimation 
of the period because of the two important reasons:
 - when plotting chi^2 values around the candidate periods, you can find that the distribution 
of the chi^2 values with respect to the trial periods is not smooth but noisy.
 - generally, the best periods found by statistical methods do not correspond to physically 
correct periods. You need to check folded light curves, and then judge whether the found period 
is reasonable or not. This problem is relevant to a common statistical issue about bias vs. 
variance. Chi^2 values reflect only variance information in your fitting with Splines.
- when chi^2 values are presented as N, the value is not meaningful. You may want to use 
either phase or multi with a refined period interval to estimate a period with a better time 
resolution.

3. What is the simple way to use the codes?
: run "./period.sh 184010-0047" in the command-line. In the file period.sh, you can find several 
options to control output files and how this multi-step method works.

4. What is the right range of candidate periods?
: the default range of trial periods is automatically derived by the codes, multi and phase, 
covering the possible minimum Nyquist frequency to the possible maximum one. However, long 
trial periods generally produces biased statistics in the periodograms, resulting in increasing 
statistics for long periods. It is necessary to check periodograms to figure out what range 
of trial periods is adequate. If you want to limit the range of "candidate periods", you can 
set the range for this in period.sh by using shell variables such as MIN_PERIOD, MAX_PERIOD, 
and CUT_MIN_MAX_PERIOD.

5. How is the method of Jackknife implemented in this program?
: the algorithm follows the suggestion given in the following paper.
  A Trustworthy Jackknife - Rupert G. Miller
  (Ann. Math. Statist. Volume 35, Number 4 (1964), 1594-1605)
Using the Jackknife estimation method is generally not necessary. Moreover, this 
method can be less reliable in many cases. If the distribution of the sample statistics is 
not close to a normal distribution, it is not recommended to use the statistics derived by 
using the Jackknife estimation method. Therefore, I recommend to use multi and 
phase withtout resampling as an intial method. When you find the range of trial periods which require 
a reliable detection or a significance estimation, you can try the implementation of 
the Jackknife estimation in the current version, and you can check the distribution of 
the Jackknife sample statistics. The codes multi and phase estimate and store only partial 
estimate values which can be used with read_plot_resample.py to derive the Jackknife mean 
estimation of periodogram statistics.
