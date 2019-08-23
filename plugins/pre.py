from . import bolflow

import logging
import pandas
import string


class preData(bolflow.bolflow):
    
    def __init__(self, i, c=None):
        self.infiles = i
        self.inclass = c
        super().__init__(None, c)

    def join(self):        
        '''
        Join the Metabolomic files into unique file
        '''
        # create df from all input files
        # get the max length of index
        idfs = []
        lmax = 1
        for infile in self.infiles:
            d = None
            logging.debug('read file '+infile)
            d = pandas.read_excel(infile, na_values=['NA'])
            d = self.__del_cols(d)
            l = len( str(d.index.argmax() + 1) )
            if l > lmax : lmax = l
            logging.debug('append file '+infile)
            idfs.append(d)
        # append dataframes
        # init with classification file
        logging.debug('init global dataframe')
        c = pandas.read_excel(self.inclass, na_values=['NA'])
        df = self.__classify(c)        
        df = df.append(pandas.Series('Max', index=df.columns), ignore_index=True)
        for idx, d in enumerate(idfs):
            logging.debug('add index')
            d = self.__add_index(d, idx, lmax)
            logging.debug('append dataframe')
            df = pandas.concat([df,d], sort=True)
        # set Name col as index
        self.df = df.set_index('Name')
        # # move the column to head of list using index, pop and insert
        # cols = list(df)
        # cols.insert(0, cols.pop(cols.index('Name')))
        # cols.insert(1, cols.pop(cols.index('RT [min]')))
        # cols.insert(2, cols.pop(cols.index('Max. Area')))
        # df = df.loc[:, cols]
        # # create csv
        # self.df.to_csv(self.outfile)

    def __classify(self, df):
        df['Samples'] = df['Samples'].str.strip() # trim whitespaces
        d = df.set_index('Samples').transpose()
        d.insert(loc=0, column='Name', value=d.index)
        d.index = range(len(d))
        return d

    def __del_cols(self, df):
        # header names that will be deleted
        cols = [ c for c in df.columns if '.raw' in c.lower() or c.lower() in ['checked','name','comments'] ]
        d = df.drop(cols, axis=1)
        # rename some headers
        d.columns = d.columns.str.replace('\s*Group Area:\s*', '')
        return d

    def __add_index(self, df, idx, l):
        i = list(string.ascii_uppercase)[idx]
        cols = [ i+str(c+1).zfill(l) for c in df.index ]
        df.insert(loc=0, column='Name', value=cols)
        return df

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
        # create csv
        self.df.to_csv(outfile)


