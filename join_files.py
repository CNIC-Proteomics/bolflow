#!/usr/bin/python
import argparse, logging, os
import subprocess

# import components for bolflow
from plugins import pre

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    logging.info('create bolflow object')
    w = pre.preData(args.infiles, args.incfile, args.outfile)
    
    logging.info('join input files')
    w.join()
    

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Join the input files for the metabolomics workflow',
        epilog='''
        Example:
            join_files.py -ii ~/indir/V1_HILIC_POS_0-6min_Original.txt ~/indir/V1_HILIC_POS_4-11min_Original.txt -ic ~/indir/Classification_V1.xlsx -o ~/outdir/V1_HILIC_POS_combined-filtered.csv
        ''')
    parser.add_argument('-ii',  '--infiles', required=True, nargs='+', help='input files for the workflow')
    parser.add_argument('-ic',  '--incfile', required=True, help='input file with the classification for the workflow')
    parser.add_argument('-o',  '--outfile', required=True, help='combined file')
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