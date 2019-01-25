#!/usr/bin/python
import argparse, logging, os
import subprocess

# import components for bolflow
from plugins import filt

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    logging.info('create bolflow object')
    w = filt.filter(args.infile)
    
    logging.info('filter the frequency (per group of samples and QCs)')
    w.filter_freq(args.ffreq, args.fcv, 'Freq')

    logging.info('filter the frequency')
    if args.rem_dup:
        w.del_dup({ 'A': [0,15], 'B': [13,28] })

    logging.info('print dataframe')
    w.to_csv(args.outfile)    


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Join the input files for the metabolomics workflow',
        epilog='''
        Example:
            filter.py -i ~/outdir/V1_HILIC_POS_combined-filtered.freq.csv -ff 80 -fcv 50 -o ~/outdir/V1_HILIC_POS_combined-filtered.freq-filt.csv
        ''')
    parser.add_argument('-i',   '--infile',  required=True, help='combined file for the workflow')
    parser.add_argument('-ff',  '--ffreq',   default=False, help='filter by the frequency of samples group. By default, none')
    parser.add_argument('-fc',  '--fcv',     default=False, help='filter for the cv. By default, none')
    parser.add_argument('-d',   '--rem_dup', default=False, help='flag that says if we remove duplicates')
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