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
        logging.debug('\n'+str(df))
        # get columns from the group and qc
        logging.debug('get columns from the group and qc')
        col = {'grp': [], 'qc': []}
        for c in fcol:
            if 'QC' in c:
                col['qc'].append(c)
            else:
                col['grp'].append(c)
        # get the comparative value from the groups and qc using the filter value
        logging.debug('get the global frequency of groups')
        grp = {}
        grp['grp'] = df.loc['Group', col['grp']].apply( lambda x: round( (int(x)*int(fvalue))/100 ) ).astype('float64')
        grp['qc']  = df.loc['Group', col['qc']].apply( lambda x: round( (int(x)*int(cvalue))/100 ) ).astype('float64')
        logging.debug('\n'+str(grp))
        # drop row when is less than the filtered percetages
        # different percentages for the group and qc
        logging.debug('drop row when is less than the filtered percetages')        
        for name,row in df.iterrows():
            if not ('Group' in name) and not ('Cohort' in name) and not ('Global' in name):
                dgrp = df.loc[name, col['grp']]
                dqc = df.loc[name, col['qc']]
                if any(dgrp < grp['grp']) and any(dqc < grp['qc']):
                    self.df.drop(name, inplace=True)
        logging.debug('\n'+str(self.df))

    def __filter_cv(self,fvalue):
        print(fvalue)
                            

    def to_csv(self,outfile):
        '''
        Print to CSV
        '''
        self.df.to_csv(outfile)





