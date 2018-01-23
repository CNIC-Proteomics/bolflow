import logging
import pandas
import string
import re

__author__ = 'jmrodriguezc'


class filter:
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i):
        self.infile = i
        self.df = pandas.read_csv(self.infile, na_values=['NA'], low_memory=False).set_index('Name')

    def filter(self, ftype, fvalue, cvalue):
        '''
        Filter the dataframe
        '''
        if ftype == 'freq':
            self.__filter_freq(fvalue, cvalue,'Freq')
        elif ftype == 'cv':
            self.__filter_cv(fvalue)
        
    def __filter_freq(self, fvalue, cvalue, prefix):
        '''
        Filter by frequency
        '''
        # get dataframe with the frequency columns by group and batch
        # discard the "blank" groups
        logging.debug('get dataframe with the frequency columns by group and batch and without "blank" groups')
        fcol = [col for col in self.df if col.startswith(prefix) and not col.startswith(prefix+'_B-') and re.search(r'\d+$', col)]        
        df = self.df[fcol]
        # get columns from the group and qc
        logging.debug('get columns from the group and qc')
        col = {'grp': [], 'qc': []}
        for c in fcol:
            if 'QC' in c:
                col['qc'].append(c)
            else:
                col['grp'].append(c)
        # create a list with the experiment names
        logging.debug('create a list with the experiment names')
        iname = [name for name in df.index if ('Cohort' not in name) and ('Group' not in name) and ('Batch' not in name) and ('Global' not in name)]
        # get the comparative value from the groups and qc using the filter value
        logging.debug('get the global frequency of groups')
        grp = {}
        grp['grp'] = df.loc['Group', col['grp']].apply( lambda x: round( (int(x)*int(fvalue))/100 ) ).astype('float64')
        grp['qc']  = df.loc['Group', col['qc']].apply( lambda x: round( (int(x)*int(cvalue))/100 ) ).astype('float64')
        # filter the values separating the groups and qc: different filter cutoff
        logging.debug('filter the values separating the groups and qc')
        dgrp = df.loc[iname, col['grp']] < grp['grp']
        dqc = df.loc[iname, col['qc']] < grp['qc']
        # create a column with the comparison for groups
        # create a column with the comparison for qc
        logging.debug('extract all experiment with false condition')
        dg = dgrp.all(axis=1)
        dq = dqc.all(axis=1)
        # join both conditions
        # delete any experiment when any condition
        logging.debug('drop the experiment')
        dc = pandas.concat([dg,dq], axis=1)
        d = dc[ dc.any(axis=1) ]
        self.df.drop(d.index, inplace=True)

    def __filter_cv(self,fvalue):
        print(fvalue)
                            

    def to_csv(self,outfile):
        '''
        Print to CSV
        '''
        self.df.to_csv(outfile)





