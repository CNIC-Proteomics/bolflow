#!/usr/bin/python
import logging
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import re
import ast
import yaml
from plugins import pre,calc,filt # import components for bolflow

__author__ = 'jmrodriguezc'

def processes(infiles, incfile, outdir, outname, step, rem_dup, ftype, ffreq, fcv):
    '''
    Execute the processes:
bolflow - Metabolomic workflow

Steps:
    1. join files and add features
    2. calculate frequency and coefficient variation
    3. remove duplicates
    4. several filters

Examples:
* all steps together:
  -s 1234  -n test1-out  -ii tests/test1-in1.xlsx tests/test1-in2.xlsx  -ic tests/test1-inC.xlsx  -o tests/  -d '{"A":[0,5], "B":[4,10]}'  -t QC  -f 50

* step 1:
  -s 1  -n test1-out  -ii tests/test1-in1.xlsx  tests/test1-in2.xlsx  -ic tests/test1-inC.xlsx  -o tests/

* step 2:
  -s 2  -n test1-out  -ii tests/test1-out.join.csv -ic tests/test1-inC.xlsx  -o tests/

* step 3:
  -s 3  -n test1-out  -ii tests/test1-out.f-cv.csv -ic tests/test1-inC.xlsx  -o tests/  -d "{'A':[0,5], 'B':[4,10]}"

* step 4:
  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t QC    -ff 50
  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t QC    -ff 50  -fc 60
  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t S     -ff 80
  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t C     -ff 80
  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t D     -ff 80
  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t C,D   -ff 80
    '''

    # check conditional parameters
    # if '3' in step and not 'rem_dump' in args:
    if '3' in step and not rem_dup:
        parser.print_help(sys.stderr)
        sys.exit("\n\nERROR: we need 'rem_dup' parameter for the step-3\n")
    if '4' in step and (not ftype or not ffreq):
        parser.print_help(sys.stderr)
        sys.exit("\n\nERROR: we need 'ftype' and 'ffreq' parameters for the step-4. 'fcv' is optional\n")

    
    # delete the last slash
    outdir = re.sub(r'\/*$','', outdir)
    # prepare workspace
    os.makedirs(outdir, exist_ok=True)
    
    # get the base name for the output file
    if outname:
        outname = '{}/{}'.format(outdir, outname)
    else:
        outname = '{}/{}'.format(outdir, 'bolflow')

    if '1' in step:
        # assign input/outputs
        outfile = '{}.{}.{}'.format(outname,'join','csv')
        logging.info('step 1: {} > {}'.format(','.join(infiles), outfile) )

        w = pre.preData(infiles, incfile)

        logging.info('join input files')
        w.join()

        logging.info('print output')
        w.to_csv(outfile)

        # reassign output file
        infile  = outfile
    else:
        infile  = infiles[0]
    
    if '2' in step:
        # assign input/outputs
        outfile = '{}.{}.{}'.format(outname,'f-cv','csv')
        logging.info('step 2: {} > {}'.format(infile, outfile))

        w = calc.calculate(infile, incfile)

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
    #     infile  = infiles[0]

    if '3' in step:
        # assign input/outputs
        outfile = '{}.{}.{}'.format(outname,'rem','csv')
        logging.info('step 3: {} > {}'.format(infile, outfile))

        w = filt.filter(infile, incfile)

        logging.info('remove duplicates')
        w.del_dup( ast.literal_eval(rem_dup) )

        logging.info('print output')
        w.to_csv(outfile)

        # reassign output file
        infile  = outfile
    # else:
    #     infile  = infiles[0]
    
    if '4' in step:
        # assign input/outputs
        outfile = '{}.{}_{}_{}_{}.{}'.format(outname,'filt',"-".join(ftype.split(',')),ffreq,'cv','csv') if fcv else '{}.{}_{}_{}.{}'.format(outname,'filt',"-".join(ftype.split(',')),ffreq,'csv')
        logging.info('step 4: {} > {}'.format(infile, outfile))
        
        w = filt.filter(infile, incfile)
        
        logging.info('filter "{}" with {}% freq. {}'.format(ftype, ffreq, 'and '+str(fcv)+'% cv' if fcv else ''))
        w.filter(ftype, ffreq, fcv)

        logging.info('print output')
        w.to_csv(outfile)


def main(args):
    ''' Main function'''

    logging.info("read parameter file")
    with open(args.parfile, 'r') as stream:
        try:
            params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            sys.exit("ERROR!! Reading the parameter file: {}".format(exc))

    processes(
        infiles=params['infiles'],
        incfile=params['incfile'],
        outdir=params['outdir'],
        step=str(params['steps']),
        rem_dup=params['remove_duplicates'],
        ftype=params['filter'],
        ffreq=params['filter_freq'],
        fcv=params['filter_cv'],
        outname=params['wfname'])
    

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description=''' bolflow - Metabolomic workflow.   

Description of parameter file:

# List of input file(s) (Excel format):
# infiles:
#   - infile_1
#   - infile_2

# Classification file (Excel format):
# incfile: clas_file

# Output directory:
# outdir: output_dir

# Name workflow:
# wfname: Name_Workflow

# bolflow - Metabolomic workflow
# 
# Steps:
#     1. join files and add features
#     2. calculate frequency and coefficient variation
#     3. remove duplicates
#     4. several filters
# eg.
# steps: 1234

# Remove duplicates ---
# remove duplicates in the samples.
# eg.
# remove_duplicates: {'A':[0,5], 'B':[4,10]}
# if you don't want to filter, write:
# remove_duplicates: false

# Filter options ---
# filter by multiple values:
# 
# Filter by the type of samples. Eg:
# filter: KO|WT
# filter: KO&WT
# filter: KO
# filter: WT
# If you don't want to filter, write
# filter: false
#
# Filter by frequency. Eg:
# filter_freq: 100
# If you don't want to filter, write
# filter_freq: false
#
# Filter by coefficient of variation. Eg:
# filter_cv: 80
# If you don't want to filter, write
# filter_cv: false


Examples:
  bolflow  -p test2/params.yml
    ''', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-p', '--parfile', required=True, help='File with the parameters for the workflow')
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