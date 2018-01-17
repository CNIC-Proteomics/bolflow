import logging
import pandas
import string

__author__ = 'jmrodriguezc'


class calculate:
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i):
        self.infile = i
        self.df = pandas.read_csv(self.infile, na_values=['NA']).set_index('Name')
        self.group_lbl = 'Group'
        g = self.df.loc[self.group_lbl].dropna().unique()
        self.qc_lbl = 'QC'
        self.group = [ c for c in g if not self.qc_lbl in c ] # discard 'QC'
        self.df_freq = None
        self.df_cv = None

    def frequency(self):
        '''
        Calculate the frequency
        '''
        # freq. based on groups
        logging.debug('freq. based on groups')
        df1 = self.__freq_a(['Group'], True)
        logging.debug('\n'+str(df1))
        # # freq. 'group' based on ALL and QC per single batch
        # logging.debug('freq. based on per single batch')
        # df1_1 = self.__freq_s(df1,'Group',['ALL'],'byFALL')
        # logging.debug('\n'+str(df1_1))
        # df1_2 = self.__freq_s(df1,'Group',['QC'],'byFQC')
        # logging.debug('\n'+str(df1_2))

        # freq. based on group-cohort
        logging.debug('freq. based on group-cohort')
        df2 = self.__freq_a(['Group','Cohort'])
        logging.debug('\n'+str(df2))
        # # freq. 'group-cohort' per single batch
        # logging.debug('freq. based on per single batch')
        # df2_1 = self.__freq_s(df2,'Group',self.group,'byFSampGroup')
        # logging.debug('\n'+str(df2_1))
        # df2_2 = self.__freq_s(df2,'Cohort Batch',self.group,'byFSampCohort')
        # logging.debug('\n'+str(df2_2))
        # df2_3 = self.__freq_s(df2,'Group',['QC'],'byFSampQC')
        # logging.debug('\n'+str(df2_3))
        
        # concat freq's
        logging.debug('concat freq\'s')
        self.df_freq = pandas.concat([df1,df2], axis=1, join_axes=[self.df.index])
        # df = pandas.concat([df1,df2,df1_1,df1_2,df2_1,df2_2,df2_3], axis=1, join_axes=[self.df.index])

        # rename columns
        logging.debug('rename colums')
        self.df_freq.columns = ['Freq_'+'-'.join(col).strip() if type(col) == tuple else 'Freq_'+str(col) for col in self.df_freq.columns.values]
        logging.debug('\n'+str(self.df_freq))
        
    def __freq_a(self,grp,all=False):
        icol = 3
        dfs = []
        for name in self.df.index:
            # extract the 'grp' columns and the actual 'name'
            g = grp[:]
            g.append(name)
            if ('Cohort' not in name) and ('Group' not in name) and ('Batch' not in name) and ('Global' not in name):
                d = self.df.loc[g].iloc[:,icol:].transpose()
                # group by 'grp' and count the frequency
                c = d.groupby(grp).count().transpose()
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
        logging.debug('\n'+str(self.df_cv))

        
    def __cv_a(self,idf):
        # get the cohort's and cohort-batch
        cohort = sorted( idf.loc['Cohort'].dropna().unique().tolist() )
        cohort_batch = sorted( idf.loc['Cohort Batch'].dropna().unique().tolist() )
        # create cv dataframe with the columns
        col = []
        for coh in cohort:
            for coh_bat in cohort_batch:
                col.append(coh+'-'+coh_bat)
            col.append(coh)
        col.append('all')
        df = pandas.DataFrame(index=self.df.index, columns=col)
        # scan every cohort and cohort-batch
        df_trans = idf.transpose()
        for coh in cohort:
            # calculate cohort-batch cv's
            for coh_bat in cohort_batch:
                # col = coh+'-'+coh_bat
                d = (df_trans['Cohort'] == coh) & (df_trans['Cohort Batch'] == coh_bat)
                c = d[d == True].index.tolist()
                # d = (df_trans['Cohort'] == coh)
                # c2 = d[d == True].index.tolist()
                # if c and c2:
                if c:
                    for name,row in idf[c].iterrows():
                        if not ('Group' in name) and not ('Cohort' in name) and not ('Global' in name):
                            row = row.astype('float64')
                            df.loc[name,(coh+'-'+coh_bat)] = (row.std() / row.mean() ) * 100
                            # row2 = row[c2].astype('float64')
                            # df.loc[name,coh] = (row2.std() / row2.mean() ) * 100
            # calculate cohort cv's
            d = (df_trans['Cohort'] == coh)
            c = d[d == True].index.tolist()
            if c:
                for name,row in idf[c].iterrows():
                    if not ('Group' in name) and not ('Cohort' in name) and not ('Global' in name):
                        row = row.astype('float64')
                        df.loc[name,coh] = (row.std() / row.mean() ) * 100
        # calculate all cv
        c = idf.columns
        if c.any():
            for name,row in idf[c].iterrows():
                if not ('Group' in name) and not ('Cohort' in name) and not ('Global' in name):
                    row = row.astype('float64')
                    df.loc[name,'all'] = (row.std() / row.mean() ) * 100
        # delete empty columns
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

        # concat all freq's
        self.df.to_csv(outfile)        


    # def __freq_s(self,idf,g,n,c):
    #     grp = idf.loc[g,n]
    #     df = pandas.DataFrame(index=self.df.index, columns=[c])
    #     for name,row in idf.iterrows():
    #         if not ('Group' in name) and not ('Cohort' in name) and not ('Global' in name):
    #             d = idf.loc[name,n]
    #             df.loc[name,c] = any(d >= grp)
    #     return df



