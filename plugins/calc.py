import logging
import pandas
import string
import re

__author__ = 'jmrodriguezc'


class calculate:
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i):
        self.infile = i
        self.df = pandas.read_csv(self.infile, na_values=['NA'], low_memory=False).set_index('Name')
        self.group_lbl = 'Group'
        g = self.df.loc[self.group_lbl].dropna().unique()
        self.qc_lbl = 'QC'
        self.group = [ c for c in g if not self.qc_lbl in c ] # discard 'QC'
        self.df_freq = None
        self.df_cv = None
        self.names = [name for name in self.df.index if re.search(r'^\w{1}\d+$', name)] # experiments

    def frequency(self):
        '''
        Calculate the frequency
        '''
        # freq. based on groups
        logging.debug('freq. based on groups')
        df1 = self.__freq_a(['Group'], True)

        # freq. based on group-cohort
        logging.debug('freq. based on group-cohort')
        df2 = self.__freq_a(['Group','Cohort'])
        
        # concat freq's
        logging.debug('concat freq\'s')
        self.df_freq = pandas.concat([df1,df2], axis=1, join_axes=[self.df.index])

        # rename columns
        logging.debug('rename colums')
        self.df_freq.columns = ['Freq_'+'-'.join(col).strip() if type(col) == tuple else 'Freq_'+str(col) for col in self.df_freq.columns.values]
        
    def __freq_a(self,grp,all=False):
        icol = 3
        dfs = []
        for name in self.df.index:
            # extract the 'grp' columns and the actual 'name'
            g = grp[:]
            g.append(name)
            if ('Cohort' not in name) and ('Group' not in name) and ('Batch' not in name) and ('Global' not in name):
                # group by 'grp' and count the frequency
                d = self.df.loc[g].iloc[:,icol:].transpose()
                c = d.groupby(grp).count().transpose()
                dfs.append(c)
            elif 'Group' == name:
               # for the same name, we have to duplicate column and rename
                d = self.df.loc[g].iloc[:,icol:].transpose()
                name_0 = name+'_0'
                d.columns.values[-1] = name_0
                c = d.groupby(grp).count().transpose()
                c = c.rename(index={name_0: name})
                dfs.append(c)                
        df = pandas.concat(dfs)
        if all:
            df.insert(loc=0, column='ALL', value=df[self.group].sum(axis=1))
        return df

    def cv(self,prefix):
        '''
        Calculate the CV = stdev / mean
        '''
        logging.debug('get the QC tags started from the given prefix')
        fcol = [col for col in self.df if col.startswith(prefix)]
        df = self.df[fcol]

        logging.debug('freq. based on groups')
        self.df_cv = self.__cv_a(df)
        
        # rename columns
        logging.debug('rename colums')
        self.df_cv.columns = ['CV_'+c for c in self.df_cv.columns.values]
        
    def __cv_a(self,idf):
        # get the cohort's and cohort-batch
        logging.debug('get the cohort\'s and cohort-batch')
        cohort = sorted( idf.loc['Cohort'].dropna().unique().tolist() )
        cohort_batch = sorted( idf.loc['Cohort Batch'].dropna().unique().tolist() )
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
                d = (df_trans['Cohort'] == coh) & (df_trans['Cohort Batch'] == coh_bat)
                c = d[d == True].index.tolist()
                if c:
                    dn = idf.loc[self.names,c].astype(float)
                    df.loc[self.names,(coh+'-'+coh_bat)] = ( dn.std(axis=1) / dn.mean(axis=1) ) * 100
            # calculate cohort cv's
            logging.debug('calculate cohort cv')
            d = (df_trans['Cohort'] == coh)
            c = d[d == True].index.tolist()
            if c:
                dn = idf.loc[self.names,c].astype(float)
                df.loc[self.names,coh] = ( dn.std(axis=1) / dn.mean(axis=1) ) * 100
        # calculate all cv
        logging.debug('calculate all cv')
        c = idf.columns
        if c.any():
            dn = idf.loc[self.names,c].astype(float)
            df.loc[self.names,'all'] = ( dn.std(axis=1) / dn.mean(axis=1) ) * 100
        # delete empty columns
        logging.debug('delete empty columns')
        df = df.dropna(axis=1, how='all')
        return df

    def to_csv(self,outfile):
        '''
        Print to CSV
        '''
        # concat all        
        if self.df_cv is not None:
            logging.debug('concat cv\'s')
            self.df = pandas.concat([self.df_cv,self.df], axis=1)
        if self.df_freq is not None:
            logging.debug('concat freq\'s')
            self.df = pandas.concat([self.df_freq,self.df], axis=1)
        # reorder columns
        cols = list(self.df)
        cols.insert(0, cols.pop(cols.index('Apex m/z')))
        cols.insert(1, cols.pop(cols.index('RT [min]')))
        cols.insert(2, cols.pop(cols.index('Max. Area')))
        self.df = self.df.loc[:, cols]
        # concat all freq's
        self.df.to_csv(outfile)



