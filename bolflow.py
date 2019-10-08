#!/usr/bin/python
import logging
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import re
import ast
from plugins import pre,calc,filt # import components for bolflow

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    # check conditional parameters
    # if '3' in args.step and not 'rem_dump' in args:
    if '3' in args.step and not args.rem_dup:
        parser.print_help(sys.stderr)
        sys.exit("\n\nERROR: we need 'rem_dup' parameter for the step-3\n")
    if '4' in args.step and (not args.ftype or not args.ffreq):
        parser.print_help(sys.stderr)
        sys.exit("\n\nERROR: we need 'ftype' and 'ffreq' parameters for the step-4. 'fcv' is optional\n")


    # delete the last slash
    outdir = re.sub(r'\/*$','', args.outdir)
    # get the base name for the output file
    if args.outname:
        outname = '{}/{}'.format(outdir, args.outname)
    else:
        outname = '{}/{}'.format(outdir, 'bolflow')

    if '1' in args.step:
        # assign input/outputs
        outfile = '{}.{}.{}'.format(outname,'join','csv')
        logging.info('step 1: {} > {}'.format(','.join(args.infiles), outfile) )

        w = pre.preData(args.infiles, args.incfile)

        logging.info('join input files')
        w.join()

        logging.info('print output')
        w.to_csv(outfile)

        # reassign output file
        infile  = outfile
    else:
        infile  = args.infiles[0]
    
    if '2' in args.step:
        # assign input/outputs
        outfile = '{}.{}.{}'.format(outname,'f-cv','csv')
        logging.info('step 2: {} > {}'.format(infile, outfile))

        w = calc.calculate(infile, args.incfile)

        logging.info('calculate the coefficient of variation')
        w.cv()

        logging.info('calculate the frequency')
        w.frequency()

        logging.info('get the maximum value')
        w.max_value()

        logging.info('print output')
        w.to_csv(outfile)

        # reassign output file
        infile  = outfile
    # else:
    #     infile  = args.infiles[0]

    if '3' in args.step:
        # assign input/outputs
        outfile = '{}.{}.{}'.format(outname,'rem','csv')
        logging.info('step 3: {} > {}'.format(infile, outfile))

        w = filt.filter(infile, args.incfile)

        logging.info('remove duplicates')
        w.del_dup( ast.literal_eval(args.rem_dup) )

        logging.info('print output')
        w.to_csv(outfile)

        # reassign output file
        infile  = outfile
    # else:
    #     infile  = args.infiles[0]
    
    if '4' in args.step:
        # assign input/outputs
        outfile = '{}.{}_{}_{}_{}.{}'.format(outname,'filt',"-".join(args.ftype.split(',')),args.ffreq,'cv','csv') if args.fcv else '{}.{}_{}_{}.{}'.format(outname,'filt',"-".join(args.ftype.split(',')),args.ffreq,'csv')
        logging.info('step 4: {} > {}'.format(infile, outfile))
        
        w = filt.filter(infile, args.incfile)
        
        logging.info('filter "{}" with {}% freq. {}'.format(args.ftype, args.ffreq, 'and '+args.fcv+'% cv' if args.fcv else ''))
        w.filter(args.ftype, args.ffreq, args.fcv)

        logging.info('print output')
        w.to_csv(outfile)

    
    

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description='''
bolflow - Metabolomic workflow

Steps:
    1. join files and add features
    2. calculate frequency and coefficient variation
    3. remove duplicates
    4. several filters

Examples:
* all steps together:
  bolflow -s 1234  -n test1-out  -ii tests/test1-in1.xlsx tests/test1-in2.xlsx  -ic tests/test1-inC.xlsx  -o tests/  -d '{"A":[0,5], "B":[4,10]}'  -t QC  -f 50

* step 1:
  bolflow -s 1  -n test1-out  -ii tests/test1-in1.xlsx  tests/test1-in2.xlsx  -ic tests/test1-inC.xlsx  -o tests/

* step 2:
  bolflow -s 2  -n test1-out  -ii tests/test1-out.join.csv -ic tests/test1-inC.xlsx  -o tests/

* step 3:
  bolflow -s 3  -n test1-out  -ii tests/test1-out.f-cv.csv -ic tests/test1-inC.xlsx  -o tests/  -d "{'A':[0,5], 'B':[4,10]}"

* step 4:
  bolflow -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t QC    -ff 50
  bolflow -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t QC    -ff 50  -fc 60
  bolflow -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t S     -ff 80
  bolflow -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t C     -ff 80
  bolflow -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t D     -ff 80
  bolflow -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t C,D   -ff 80
        ''', formatter_class=RawTextHelpFormatter)

    required = parser.add_argument_group('required arguments')
    conditional = parser.add_argument_group('conditional arguments')

    required.add_argument('-s',  '--step',    required=True, help='Step workflow: 1-join files, 2-calculate freq. and cv, 3-remove duplicates, 4-filters. Eg. 1234')
    required.add_argument('-ii', '--infiles', required=True, nargs='+', help='input file(s) for the workflow')
    required.add_argument('-ic', '--incfile', required=True, help='input file with the classification for the workflow')
    required.add_argument('-o',  '--outdir',  required=True, help='output directory')
    
    conditional.add_argument('-d',  '--rem_dup', help='for step-2: json with the times for each group. Eg, {"A":[0,4], "B":[3,8], "C":[7,12]}')
    conditional.add_argument('-t',  '--ftype',   help='for step-3: filter type depending on the classification file. Eg. QC (quality control), S (biological sample), C (control group), D (disease group)')
    conditional.add_argument('-ff', '--ffreq',   help='for step-3: filter value of frequency. By default, none')
    conditional.add_argument('-fc', '--fcv',     help='for step-3: filter value of coefficient of variation. By default, none')

    parser.add_argument('-n',  '--outname', help='prefix name of output files')
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

    logging.info('start script: '+"{0}".format(" ".join([x for x in sys.argv])))
    main(args)
    logging.info('end '+os.path.basename(__file__))