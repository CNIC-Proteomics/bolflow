import argparse, logging, os
import subprocess

# import components for bolflow
from plugins import filt

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    logging.info('create bolflow object')
    w = filt.filter(args.infile)
    
    logging.info('filter the frequency')
    w.filter('freq', args.ffreq, args.fcv)

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
    parser.add_argument('-ff',  '--ffreq',   default=80, help='filter for the frequency')
    parser.add_argument('-fc',  '--fcv',     default=50, help='filter for the cv')
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