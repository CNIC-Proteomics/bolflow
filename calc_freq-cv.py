#!/usr/bin/python
import argparse, logging, os

# import components for bolflow
from plugins import calc

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    logging.info('create bolflow object')
    w = calc.calculate(args.infile, args.incfile)
    
    logging.info('calculate the coefficient of variation')
    w.cv()

    logging.info('calculate the frequency')
    w.frequency()

    logging.info('get the maximum value')
    w.max_value()

    logging.info('print dataframe')
    w.to_csv(args.outfile)


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Join the input files for the metabolomics workflow',
        epilog='''
        Example:
            frequency.py -i ~/outdir/V1_HILIC_POS_combined-filtered.join.csv -qc C18_QC -o ~/outdir/V1_HILIC_POS_combined-filtered.freq.csv
        ''')
    parser.add_argument('-i',  '--infile',  required=True, help='joined file for the workflow')
    parser.add_argument('-ic', '--incfile', required=True, help='input file with the classification for the workflow')
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