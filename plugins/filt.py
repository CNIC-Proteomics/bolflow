from . import bolflow

import logging
import pandas
import re

__author__ = 'jmrodriguezc'

class filter(bolflow.bolflow):
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i, c=None):
        super().__init__(i, c)


    def filter(self, ftype, ffreq, fcv):
        '''
        Filter by frequency
        '''
        # get the comparative value from the groups and qc using the filter value
        # get dataframe with the frequency columns
        # if QC then get the CV_all column
        logging.debug('get dataframe with the frequency columns and cv if apply')
        if fcv:
            # get columns
            fcol,ccol = [],[]
            for ft in ftype.split(","):
                fcol += [col for col in self.df if col == 'Freq_'+ft]            
            ccol = [col for col in self.df if col == 'CV_all']
            # filter columns
            if fcol and ccol:
                logging.debug('filter the frequency and cv')
                self.df = self._filter_freq_cv(fcol,ffreq,ccol,fcv)
        else:
            # get columns
            fcol = []
            for ft in ftype.split(","):
                fcol += [col for col in self.df if col == 'Freq_'+ft]
            # filter columns
            if fcol:
                logging.debug('filter the frequency')
                self.df = self._filter_freq(fcol,ffreq)

    def _filter_freq(self, fcol, fvalue):
        '''
        Filter by frequency
        '''
        df = self.df[fcol]
        # get the comparative value from the groups and qc using the filter value        
        grp = df.loc[self.title_max].apply( lambda x: round( (int(x)*int(fvalue))/100 ) ).astype('float64')
        # filter the values separating the groups and qc: different filter cutoff
        dc = df.loc[self.exps] < grp
        # delete any experiment when all conditions don't pass the filter
        d = dc[ dc.all(axis=1) ]
        df = self.df.drop(d.index.values)
        return df

    def _filter_freq_cv(self, fcol, ffreq, ccol, fcv):
        '''
        Filter by frequency
        '''
        df_g = self.df[fcol]
        df_c = self.df[ccol]
        # get the comparative value from the groups and qc using the filter value        
        grp = df_g.loc[self.title_max].apply( lambda x: round( (int(x)*int(ffreq))/100 ) ).astype('float64')
        qc  = df_c.loc[self.title_max].apply( lambda x: round( (int(x)*int(fcv))/100 ) ).astype('float64')
        # filter the values separating the groups and qc: different filter cutoff
        dc_g = df_g.loc[self.exps] < grp
        dc_c = df_c.loc[self.exps] < qc
        # delete any experiment when all conditions don't pass the filter
        g = dc_g[ dc_g.all(axis=1) ]
        c = dc_c[ dc_c.all(axis=1) ]
        # join and delete any experiments
        dc = pandas.concat([g,c], axis=1, sort=False)
        d = dc[ dc.any(axis=1) ]
        df = self.df.drop(d.index.values)
        return df

    def del_dup(self, overtimes):
        '''
        Remove dupplicates
        '''
        # get the needed columns
        c = ['Freq_ALL', 'CV_all', 'Apex m/z', 'RT [min]']
        df = self.df.loc[self.exps, c]
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
        if 'Duplicate' in df:
            self.df.insert(loc=0, column='Duplicate', value=df['Duplicate'])

    def to_csv(self,outfile):
        '''
        Print to CSV
        '''
        self.df.to_csv(outfile)

