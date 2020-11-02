#!/usr/bin/env python3

# Developed by Min-Su Shin (msshin@kasi.re.kr).

import argparse
import sys
import math
import configparser
import ast
import logging

import numpy

from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import vstack, unique

from astroquery.vizier import Vizier

import matplotlib.pyplot as pyplot

max_timeout = 300 # seconds <--- Default timeout for connecting to server

max_row_limit = -1 # unlimited <-- Maximum number of rows that will be fetched from the result (set to -1 for unlimited).
histogram_bin = 0.05 # deg
server_dict = {'cds': 'vizier.u-strasbg.fr', 'cadc': 'vizier.hia.nrc.ca', \
'cam': 'vizier.ast.cam.ac.uk', 'cfa': 'vizier.cfa.harvard.edu'}

def run_query(use_vizier_object, use_skycoord, use_width, use_height):
    try:
        print("... accessing Vizier")
        query_object = use_vizier_object.query_region(coordinates=use_skycoord, 
        width=use_width, height=use_height)
    except:
        print('[ERROR] query_region failed.', file=sys.stderr)
        sys.exit(1)
    if len(query_object) == 0:
        print("[WARNING] there is no output from the Vizier catalog. Probably, the area is not covered by the catalog.")
        return None
    else:
        print(".. the number of objects in the retrieved data: %d" % (len(query_object[0])))
        return query_object[0]

arg_parser = argparse.ArgumentParser(description = \
'Download reference catalogs for QC from Vizier', allow_abbrev=False)

# option to use configuration file instead of command-line options
arg_parser.add_argument('--config', action='store', nargs='?', \
type=str, required=False, help='configuration filename for the catalog')

arg_parser.add_argument('--output', action='store', nargs='?', type=str, \
required=True, help='the output ascii filename')
arg_parser.add_argument('--plot', default=False, action='store_true', \
help='producing the plot showing RA, DEC ranges')

arg_parser.add_argument('--catalog', choices=['gaiadr2', 'gaiadr2_G', 'psdr1_r', 'psdr1', \
'smssdr1.1_r', 'smssdr1.1', 'vhsdr4'], required=False, \
help='the reference catalog: gaiadr2_G = Gaia DR2 with G-mag, gaiadr2 = Gaia DR2, psdr1_r = Pan-STARRS DR1 with r-mag, psdr1 = Pan-STARRS DR1, smssdr1.1_r = SkyMapper Southern Sky Survey DR1.1 with r-mag, smssdr1.1 = SkyMapper Southern Sky Survey DR1.1, vhsdr4 = VISTA Hemisphere Survey DR4')
# one way to set the spatial range
arg_parser.add_argument('--min_ra', action='store', nargs='?', type=float)
arg_parser.add_argument('--max_ra', action='store', nargs='?', type=float)
arg_parser.add_argument('--min_dec', action='store', nargs='?', type=float)
arg_parser.add_argument('--max_dec', action='store', nargs='?', type=float)
# another way to set the spatial range
arg_parser.add_argument('--center_ra', action='store', nargs='?', type=float)
arg_parser.add_argument('--width_ra', action='store', nargs='?', type=float)
arg_parser.add_argument('--center_dec', action='store', nargs='?', type=float)
arg_parser.add_argument('--width_dec', action='store', nargs='?', type=float)
# option to filter out sources out of the required ranges
arg_parser.add_argument('--filter', default=False, action='store_true', \
help='filtering out the sources out of the required search range')
# option to filter out specific box area
arg_parser.add_argument('--exbox_min_ra', action='store', nargs='?', \
type=float, required=False, help='filtering out the sources in the box range')
arg_parser.add_argument('--exbox_max_ra', action='store', nargs='?', \
type=float, required=False, help='filtering out the sources in the box range')
arg_parser.add_argument('--exbox_min_dec', action='store', nargs='?', \
type=float, required=False, help='filtering out the sources in the box range')
arg_parser.add_argument('--exbox_max_dec', action='store', nargs='?', \
type=float, required=False, help='filtering out the sources in the box range')
# way to ing a large FOV
arg_parser.add_argument('--stitch', action='store', default=-1.0, type=float, \
help='stitching a large field with a given step width (deg)')
# server
arg_parser.add_argument('--server', action='store', default='cds', \
choices=['cds', 'cadc', 'cam', 'cfa'], required=False)
# verbose
arg_parser.add_argument('--verbose', default=False, action='store_true', \
help='verbose output for debugging')

use_args = arg_parser.parse_args()
if use_args.catalog is None and use_args.config is None:
    arg_parser.print_help()
    sys.exit(1)

if use_args.verbose:
    logging.basicConfig(level='DEBUG')
else:
    logging.basicConfig(level='ERROR')

if use_args.config is not None:
    use_config = configparser.ConfigParser()
    try:
        use_config.read(use_args.config)
    except:
        print("[ERROR] %s is not accessible." % (use_args.config))
        sys.exit(1)
    use_catalog = use_config['Catalog']['name']
    use_catalog_vizier = use_config['Catalog']['vizier']
    use_catalog_columns = ast.literal_eval(use_config['Catalog']['columns'])
    use_catalog_ID = use_config['Key']['ID']
    use_catalog_RA = use_config['Key']['RA']
    use_catalog_DEC = use_config['Key']['DEC']
else:
    use_catalog = use_args.catalog

if use_args.center_ra is None and use_args.min_ra is None:
    arg_parser.print_help()
    sys.exit(1)
elif use_args.center_ra is None:
    if use_args.max_ra is None or use_args.min_dec is None or \
    use_args.max_dec is None:
        arg_parser.print_help()
        sys.exit(1)
    else:
        center_ra = 0.5*(use_args.max_ra + use_args.min_ra)
        center_dec = 0.5*(use_args.max_dec + use_args.min_dec)
        width_ra = use_args.max_ra - use_args.min_ra
        width_dec = use_args.max_dec - use_args.min_dec
elif use_args.min_ra is None:
    if use_args.center_dec is None or use_args.width_ra is None or \
    use_args.width_dec is None:
        arg_parser.print_help()
        sys.exit(1)
    else:
        center_ra = use_args.center_ra
        center_dec = use_args.center_dec
        width_ra = use_args.width_ra
        width_dec = use_args.width_dec
else:
    arg_parser.print_help()
    sys.exit(1)

req_min_RA = center_ra - 0.5*width_ra
req_max_RA = center_ra + 0.5*width_ra
req_min_DEC = center_dec - 0.5*width_dec
req_max_DEC = center_dec + 0.5*width_dec
outfn = use_args.output

use_server = server_dict[use_args.server]
print('... using the server %s' % (use_server))

ID_key = None
RA_key = None
DEC_key = None
if use_catalog == 'gaiadr2':
    vizier_object = Vizier(columns=['Source', 'RA_ICRS', 'DE_ICRS'], 
    catalog="I/345/gaia2", row_limit=max_row_limit, vizier_server=use_server, timeout=max_timeout)
    ID_key = 'Source'
    RA_key = 'RA_ICRS'
    DEC_key = 'DE_ICRS'
elif use_catalog == 'gaiadr2_G':
    vizier_object = Vizier(columns=['Source', 'RA_ICRS', 'DE_ICRS', 
    'Gmag', 'e_Gmag', 'bp_rp'], catalog="I/345/gaia2", column_filters={"Gmag":"!="}, 
    row_limit=max_row_limit, vizier_server=use_server, timeout=max_timeout)
    ID_key = 'Source'
    RA_key = 'RA_ICRS'
    DEC_key = 'DE_ICRS'
elif use_catalog == 'psdr1':
    vizier_object = Vizier(columns=['objID', 'RAJ2000', 'DEJ2000'], 
    catalog="II/349/ps1", column_filters={"objID":"!="}, \
    row_limit=max_row_limit, vizier_server=use_server, timeout=max_timeout)
    ID_key = 'objID'
    RA_key = 'RAJ2000'
    DEC_key = 'DEJ2000'
elif use_catalog == 'psdr1_r':
    vizier_object = Vizier(columns=['objID', 'RAJ2000', 'DEJ2000', 
    'rmag', 'e_rmag'], catalog="II/349/ps1", column_filters={"rmag":"!="},
    row_limit=max_row_limit, vizier_server=use_server, timeout=max_timeout)
    ID_key = 'objID'
    RA_key = 'RAJ2000'
    DEC_key = 'DEJ2000'
elif use_catalog == 'smssdr1.1':
    vizier_object = Vizier(columns=['ObjectId', 'RAICRS', 'DEICRS'], 
    catalog="II/358/smss", column_filters={"ObjectId":"!="}, \
    row_limit=max_row_limit, vizier_server=use_server, timeout=max_timeout)
    ID_key = 'ObjectId'
    RA_key = 'RAICRS'
    DEC_key = 'DEICRS'
elif use_catalog == 'smssdr1.1_r':
    vizier_object = Vizier(columns=['ObjectId', 'RAICRS', 'DEICRS', 
    'rPetro', 'e_rPetro'], catalog="II/358/smss", column_filters={"rPetro":"!="},
    row_limit=max_row_limit, vizier_server=use_server, timeout=max_timeout)
    ID_key = 'ObjectId'
    RA_key = 'RAICRS'
    DEC_key = 'DEICRS'
elif use_catalog == 'vhsdr4':
    vizier_object = Vizier(columns=['Name', 'RAJ2000', 'DEJ2000'], 
    catalog="II/359/vhs_dr4", row_limit=max_row_limit, timeout=max_timeout)
    ID_key = 'Name'
    RA_key = 'RAJ2000'
    DEC_key = 'DEJ2000'
else:
    vizier_object = Vizier(columns=use_catalog_columns, 
    catalog=use_catalog_vizier, row_limit=max_row_limit, timeout=max_timeout)
    ID_key = use_catalog_ID
    RA_key = use_catalog_RA
    DEC_key = use_catalog_DEC

result_table = None
if use_args.stitch < 0.0:
    use_skycoord = SkyCoord(ra=center_ra*u.degree, dec=center_dec*u.degree, frame='icrs')
    use_width = u.Quantity(width_ra, u.deg)
    use_height = u.Quantity(width_dec, u.deg)
    result_table = run_query(vizier_object, use_skycoord, use_width, use_height)
    if result_table is not None:
        print('... the number of objects: ', len(result_table))
    else:
        print('... the number of objects: ', 0)
        sys.exit(0)
else:
    stitch_step = use_args.stitch
    print("... working in stitching mode with step size %f" % (stitch_step))
    num_x_bin = math.ceil((req_max_RA - req_min_RA) / stitch_step)
    num_y_bin = math.ceil((req_max_DEC - req_min_DEC) / stitch_step)
    use_width = u.Quantity(stitch_step, u.deg)
    use_height = u.Quantity(stitch_step, u.deg)
    total_number_of_queries = num_x_bin*num_y_bin
    cnt = 0
    for ind_x in range(0, num_x_bin):
        for ind_y in range(0, num_y_bin):
            print("...... %d/%d" % (cnt+1, total_number_of_queries))
            center_ra = req_min_RA + (ind_x+0.5)*stitch_step
            center_dec = req_min_DEC + (ind_y+0.5)*stitch_step
            use_skycoord = SkyCoord(ra=center_ra*u.degree, dec=center_dec*u.degree, frame='icrs')
            local_result_table = \
            run_query(vizier_object, use_skycoord, use_width, use_height)
            logging.debug('...... center_ra ' + str(center_ra) + \
            ' center_dec ' + str(center_dec) + ' use_width ' + str(use_width) + \
            ' use_height ' + str(use_height))
            if result_table is None:
                if local_result_table is not None:
                    result_table = local_result_table
                    logging.debug(local_result_table.pprint(max_lines=2))
            else:
                if local_result_table is not None:
                    result_table = vstack([result_table, local_result_table])
                    logging.debug(local_result_table.pprint(max_lines=2))
            cnt = cnt + 1
    if result_table is None:
        print('... the number of objects: ', 0)
        sys.exit(0)
    print('... the number of objects before uniquing: ', len(result_table))
#    result_table = unique(result_table, keys=ID_key)
    result_table = unique(result_table, keys=ID_key, silent=True)
    print('... the number of objects after uniquing: ', len(result_table))

if use_args.filter:
    print('... the number of objects before filtering: ', len(result_table))
    RA_filter1 = result_table[RA_key] >= req_min_RA
    RA_filter2 = result_table[RA_key] <= req_max_RA
    DEC_filter1 = result_table[DEC_key] >= req_min_DEC
    DEC_filter2 = result_table[DEC_key] <= req_max_DEC
    RA_filter = numpy.logical_and(RA_filter1, RA_filter2)
    DEC_filter = numpy.logical_and(DEC_filter1, DEC_filter2)
    use_filter = numpy.logical_and(RA_filter, DEC_filter)
    result_table = result_table[use_filter]
    print('... the number of objects after filtering: ', len(result_table))

if (use_args.exbox_min_ra is not None) and (use_args.exbox_max_ra is not None) \
and (use_args.exbox_min_dec is not None) and \
(use_args.exbox_max_dec is not None):
    print('... the number of objects before box filtering: ', len(result_table))
    RA_filter1 = result_table[RA_key] >= use_args.exbox_min_ra
    RA_filter2 = result_table[RA_key] <= use_args.exbox_max_ra
    DEC_filter1 = result_table[DEC_key] >= use_args.exbox_min_dec
    DEC_filter2 = result_table[DEC_key] <= use_args.exbox_max_dec
    RA_filter = numpy.logical_and(RA_filter1, RA_filter2)
    DEC_filter = numpy.logical_and(DEC_filter1, DEC_filter2)
    use_filter = numpy.invert(numpy.logical_and(RA_filter, DEC_filter))
    result_table = result_table[use_filter]
    print('... the number of objects after box filtering: ', len(result_table))

print('... table_summary:')
print(result_table.info)
print("... writing %s" % (outfn))
result_table.write(outfn, format='ascii.csv', overwrite=True)

RA = result_table[RA_key]
DEC = result_table[DEC_key]
print('... checking the results')
min_RA = min(RA)
max_RA = max(RA)
min_DEC = min(DEC)
max_DEC = max(DEC)
print("... required min. & max. RA :", req_min_RA, req_max_RA)
print("... required min. & max. DEC :", req_min_DEC, req_max_DEC)
print("... derived min. & max. RA :", min_RA, max_RA)
print("... derived min. & max. DEC :", min_DEC, max_DEC)
print("---> check RA: derived_min_RA - required_min_RA =", min_RA - req_min_RA)
print("--->           derived_max_RA - required_max_RA =", max_RA - req_max_RA)
print("---> check DEC: derived_min_DEC - required_min_DEC =", min_DEC - req_min_DEC)
print("--->            derived_max_DEC - required_max_DEC =", max_DEC - req_max_DEC)

if use_args.plot:
    plotfn = outfn + ".png"
    print('... producing %s' % (plotfn))
    num_x_bin = math.ceil((req_max_RA - req_min_RA) / histogram_bin)
    num_y_bin = math.ceil((req_max_DEC - req_min_DEC) / histogram_bin)
    pyplot.figure(figsize=(8,6))
    pyplot.hist2d(RA, DEC, bins=[num_x_bin, num_y_bin], range=[[req_min_RA, req_max_RA], [req_min_DEC, req_max_DEC]], cmin=0, cmap='jet')
    pyplot.xlabel('RA (deg)')
    pyplot.ylabel('DEC (deg)')
    pyplot.title('bin size = %.2f deg' % (histogram_bin))
    cbar = pyplot.colorbar()
    cbar.set_label('Number')
    pyplot.tight_layout()
    pyplot.savefig(plotfn, dpi=120)
