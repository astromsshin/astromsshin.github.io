#################################################
# Simple tools for Simbad batch jobs            #
#                                               #
# Developed by Min-Su Shin (Department of       #
# Astrophysical Sciences, Princeton University) #
#################################################

The bash shell scripts use curl command to submit the 
query files to Simbad. The default coordinate search radius 
is 6 arcsec in the Python code that produce query files.

----------------------------------------------------------

CASE I : when you have a small number of query coordinates,
the following instruction works with the relevant codes.

When you have a file coord.list that has three columns where 
the second and third columns are RA and DEC in degree, 
resepectively,

(Step 1)
./simbad_query_builder.py coord.list > coord.query

(Step 2)
./simbad_script_submit.sh coord.query coord.simbad

(Step 3)
./simbad_query_postprocess.py coord.simbad coord.simbad.result

Requirements: simbad_script_submit.sh uses the curl command. 
The change of any parts for your job is possible based on
explanation of how Simbad understands your query which 
is given in
http://simbad4.cfa.harvard.edu:8080/simbad/sim-help?Page=sim-fscript

WARNING : the script mode of Simbad limits the number of query objects.

----------------------------------------------------------

CASE II : when you have to query a substational number of objects 
to Simbad, the following codes split the queries into several pieces 
and extract the query results.

(Step 1)
./simbad_query_builder_split.py coord.list_long simbad_query

(Step 2)
./simbad_script_submit_split.sh simbad_query simbad_result_part

(Step 3)
./simbad_query_postprocess_split.py simbad_result_part 5 simbad_result
where 5 is the number of query files.
