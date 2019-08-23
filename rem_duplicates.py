#!/usr/bin/python
import argparse, logging, os
import json

# import components for bolflow
from plugins import filt

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    logging.info('create bolflow object')
    w = filt.filter(args.infile)
    
    logging.info('remove duplicates')
    w.del_dup( json.loads(args.rem_dup) )

    logging.info('print dataframe')
    w.to_csv(args.outfile)    


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Join the input files for the metabolomics workflow',
        epilog='''
        Example:
            rem_duplicates.py -i ~/outdir/V1_HILIC_POS_combined-filtered.freq.csv -d '{"A":[0,4], "B":[3,8], "C":[7,12] }' -o ~/outdir/V1_HILIC_POS_combined-filtered.rem_dup.csv
        ''')
    parser.add_argument('-i',   '--infile',  required=True, help='combined file for the workflow')
    parser.add_argument('-d',   '--rem_dup', required=True, help='json with the times for each group. Eg, {"A":[0,4], "B":[3,8], "C":[7,12]}')
    parser.add_argument('-o',   '--outfile', required=True, help='filtered file')
    parser.add_argument('-v', dest='verbose', action='store_true', help="Increase output verbosity")
    args = parser.parse_args()

    # logging debug level. By default, info level
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info('start '+os.path.basename(__file__))
    main(args)
    logging.info('end '+os.path.basename(__file__))