from . import bolflow

import logging
import pandas
import string
import re

__author__ = 'jmrodriguezc'


class calculate(bolflow.bolflow):
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i, c=None):
        super().__init__(i, c)

    def cv(self):
        '''
        Calculate the CV = stdev / mean
        '''
        logging.debug('get the QC tags started from the given tag_qc')
        df = self.df[self.samples_qc]

        logging.debug('freq. based on groups')
        df_cv = self.__cv_a(df)
        
        # rename columns
        logging.debug('rename colums')
        df_cv.columns = ['CV_'+c for c in df_cv.columns.values]

        logging.debug('concat files')
        self.df = pandas.concat([df_cv,self.df], axis=1, sort=False)
        
    def __cv_a(self,idf):
        # get the cohort's and cohort-batch
        logging.debug('get the cohort\'s and cohort-batch')
        cohort = sorted( idf.loc[self.title_cohort].dropna().unique().tolist() )
        cohort_batch = sorted( idf.loc[self.title_bat_cohort].dropna().unique().tolist() )
        # create cv dataframe with the columns
        logging.debug('create cv dataframe with the columns')
        col = []
        for coh in cohort:
            for coh_bat in cohort_batch:
                col.append(coh+'-'+coh_bat)
            col.append(coh)
        col.append('all')
        df = pandas.DataFrame(index=self.df.index, columns=col)
        # scan every cohort and cohort-batch
        logging.debug('scan every cohort and cohort-batch')
        df_trans = idf.transpose()
        for coh in cohort:
            # calculate cohort-batch cv's
            logging.debug('calculate cohort-batch cv\'s')
            for coh_bat in cohort_batch:
                d = (df_trans[self.title_cohort] == coh) & (df_trans[self.title_bat_cohort] == coh_bat)
                c = d[d == True].index.tolist()
                if c:
                    dn = idf.loc[self.exps,c].astype(float)
                    df.loc[self.exps,(coh+'-'+coh_bat)] = ( dn.std(axis=1) / dn.mean(axis=1) ) * 100
            # calculate cohort cv's
            logging.debug('calculate cohort cv')
            d = (df_trans[self.title_cohort] == coh)
            c = d[d == True].index.tolist()
            if c:
                dn = idf.loc[self.exps,c].astype(float)
                df.loc[self.exps,coh] = ( dn.std(axis=1) / dn.mean(axis=1) ) * 100
        # calculate all cv
        logging.debug('calculate all cv')
        c = idf.columns
        if c.any():
            dn = idf.loc[self.exps,c].astype(float)
            df.loc[self.exps,'all'] = ( dn.std(axis=1) / dn.mean(axis=1) ) * 100
            # assgin max value of CV all
            # df.loc['Max','all'] = df['all'].max()
        # delete empty columns
        logging.debug('delete empty columns')
        df = df.dropna(axis=1, how='all')
        return df


    def frequency(self):
        '''
        Calculate the frequency
        '''
        logging.debug('freq. of qc')
        if self.samples_qc:
            df1 = self.__freq_a([self.title_stype], discard_lbl=[self.lbl_sample,self.lbl_blank])
        else:
            df1 = None

        logging.debug('freq. of sample types')
        df2 = self.__freq_a([self.title_stype], discard_lbl=[self.lbl_qc])

        logging.debug('freq. of groups')
        df3 = self.__freq_a([self.title_group], discard_lbl=[self.lbl_qc,self.lbl_blank], all=True)

        logging.debug('freq. of group-cohort')
        df4 = self.__freq_a([self.title_group,self.title_cohort], discard_lbl=[self.lbl_qc])

        # concat freq's
        logging.debug('concat files')
        df_freq = pandas.concat([df1,df2,df3,df4], axis=1, join_axes=[self.df.index], sort=False)
        # remove duplicate columns
        df_freq = df_freq.loc[:,~df_freq.columns.duplicated()]
        # concat with the main df
        self.df = pandas.concat([df_freq,self.df], axis=1, sort=False)

        
    def __freq_a(self, grp, discard_lbl=None, all=False):
        # group by 'grp' and count the frequency (discarding the qc)
        d = self.df.loc[grp+self.exps].transpose()
        df = d.groupby(grp).count().transpose()
        # discard labels
        for l in discard_lbl:
            if l in df.columns:
                df.drop(columns=l, inplace=True)
        # add frequency of all elements
        if all:
            df.insert(loc=0, column='ALL', value=df.sum(axis=1))
        # add the maximum value at the beginning
        df.loc['Max'] = df.max()
        # rename columns with prefix
        df.columns = ['Freq_'+'-'.join(col).strip() if type(col) == tuple else 'Freq_'+str(col) for col in df.columns.values]
        return df


    def max_value(self):
        '''
        Extract the maximum value of all experiments
        '''
        df = self.df.loc[self.exps]
        df = df.astype(float)
        self.df.loc['Max'] = df.max()


    def to_csv(self,outfile):
        '''
        Print to CSV
        '''
        # reorder columns
        cols = list(self.df)
        cols.insert(0, cols.pop(cols.index(self.incol_mz)))
        cols.insert(1, cols.pop(cols.index(self.incol_rt)))
        cols.insert(2, cols.pop(cols.index(self.incol_max_area)))
        self.df = self.df.loc[:, cols]
        # concat all freq's
        self.df.to_csv(outfile)



