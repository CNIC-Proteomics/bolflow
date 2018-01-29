import logging
import pandas
import string
import re
# import math 

__author__ = 'jmrodriguezc'


class filter:
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i):
        self.infile = i
        self.df = pandas.read_csv(self.infile, na_values=['NA'], low_memory=False).set_index('Name')

    def filter_freq(self, fvalue, cvalue, prefix='Freq'):
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
        inames = [name for name in df.index if ('Cohort' not in name) and ('Group' not in name) and ('Batch' not in name) and ('Global' not in name)]
        # get the comparative value from the groups and qc using the filter value
        logging.debug('get the global frequency of groups')
        grp = {}
        grp['grp'] = df.loc['Group', col['grp']].apply( lambda x: round( (int(x)*int(fvalue))/100 ) ).astype('float64')
        grp['qc']  = df.loc['Group', col['qc']].apply( lambda x: round( (int(x)*int(cvalue))/100 ) ).astype('float64')
        # filter the values separating the groups and qc: different filter cutoff
        logging.debug('filter the values separating the groups and qc')
        dgrp = df.loc[inames, col['grp']] < grp['grp']
        dqc = df.loc[inames, col['qc']] < grp['qc']
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


    def del_dup(self, overtimes):
        '''
        Remove dupplicates
        '''
        # get the needed columns
        c = ['Freq_ALL', 'CV_all', 'Apex m/z', 'RT [min]']
        inames = [name for name in self.df.index if ('Cohort' not in name) and ('Group' not in name) and ('Batch' not in name) and ('Global' not in name)]
        df = self.df.loc[inames, c]
        # find the duplicated experiments:        
        # - sort by Apex m/z and times
        df = df.sort_values(by=['Apex m/z', 'RT [min]'])
        # - mass very similar and times close
        df['Apex m/z shift'] = df['Apex m/z'].shift(-1)
        df['RT [min] shift'] = df['RT [min]'].shift(-1)
        df['m/z_time_cmp'] = (abs(df['Apex m/z'] - df['Apex m/z shift']) < 0.0001) & (abs(df['RT [min]'] - df['RT [min] shift']) < 0.1)
        dups = df.index[df['m/z_time_cmp']].tolist()
        for dup in dups:
            idx = df.index.get_loc(dup)
            dup_nxt = df.index[min(idx+1, len(df)-1)]      
            # check if exp. comes from different names
            if dup[:1] != dup_nxt[:1]:
                t = df.loc[dup, 'RT [min]']
                lbl = None
                for prefix,times in overtimes.items():
                    if (t >= times[0] and t <= times[1]):
                        # label the another exp.
                        if prefix == dup[:1]:
                            lbl = dup_nxt
                        elif prefix == dup_nxt[:1]:
                            lbl = dup                            
                        break
                # select the experiment based on RT [min]:
                # - [0, 4.5]  => first file
                # - [5, 11] => second file
                # - (4.5, 5) => check
                #   - freq to all >
                #   - < cv%
                if lbl is None:
                    if ( df.loc[dup, 'Freq_ALL'] > df.loc[dup_nxt, 'Freq_ALL'] ):
                        lbl = dup_nxt
                    elif ( df.loc[dup, 'Freq_ALL'] < df.loc[dup_nxt, 'Freq_ALL'] ):
                        lbl = dup
                    else:
                        if ( df.loc[dup, 'CV_all'] < df.loc[dup_nxt, 'CV_all'] ):
                            lbl = dup_nxt
                        elif ( df.loc[dup, 'CV_all'] >= df.loc[dup_nxt, 'CV_all'] ):
                            lbl = dup                
                df.loc[lbl, 'Duplicate'] = 'YES'
        self.df.insert(loc=0, column='Duplicate', value=df['Duplicate'])

    def to_csv(self,outfile):
        '''
        Print to CSV
        '''
        self.df.to_csv(outfile)

