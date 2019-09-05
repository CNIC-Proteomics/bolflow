#!/usr/bin/python
import argparse, logging, os

# import components for bolflow
from plugins import filt

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    logging.info('create bolflow object')
    w = filt.filter(args.infile, args.incfile)
    
    logging.info('filter "{}" with {}% freq. {}'.format(args.ftype, args.ffreq, 'and '+args.fcv+'% cv' if args.fcv else ''))
    w.filter(args.ftype, args.ffreq, args.fcv)

    logging.info('print output')
    w.to_csv(args.outfile)


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Join the input files for the metabolomics workflow',
        epilog='''
        Example:
            filter.py -i ~/outdir/V1_HILIC_POS_combined-filtered.freq.csv -t qc -f 50 -o ~/outdir/V1_HILIC_POS_combined-filtered.freq-filt.csv
        ''')
    parser.add_argument('-ii',  '--infile',  required=True, help='combined file for the workflow')
    parser.add_argument('-ic', '--incfile', required=True, help='input file with the classification for the workflow')
    parser.add_argument('-t',  '--ftype',   help='for step-3: filter type depending on the classification file. Eg. QC (quality control), S (biological sample), C (control group), D (disease group)')
    parser.add_argument('-ff', '--ffreq',   help='for step-3: filter value of frequency. By default, none')
    parser.add_argument('-fc', '--fcv',     help='for step-3: filter value of coefficient of variation. By default, none')
    parser.add_argument('-o',  '--outfile', required=True, help='filtered file')
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