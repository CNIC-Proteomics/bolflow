import pandas
import string

__author__ = 'jmrodriguezc'


class preData:
    '''
    Make the data pre-processing in the workflow
    '''
    def __init__(self, i, c, o):
        self.infiles = i
        self.inclass = c
        self.outfile = o
        self.df = None

    def join(self):        
        '''
        Join the Metabolomic files into unique file
        '''
        dfs = []
        # init with classification file
        c = pandas.read_excel(self.inclass, na_values=['NA'])
        dfs.append(self.__classify(c))
        # append dataframes
        for idx, infile in enumerate(self.infiles):
            d = pandas.read_excel(infile, na_values=['NA'])
            # delete cols
            d = self.__del_cols(d)
            # create index
            d = self.__add_index(d, idx)
            dfs.append(d)    
        # merge dfs
        df = pandas.concat(dfs)
        # move the column to head of list using index, pop and insert
        cols = list(df)
        cols.insert(0, cols.pop(cols.index('Name')))
        cols.insert(2, cols.pop(cols.index('RT [min]')))
        cols.insert(3, cols.pop(cols.index('Max. Area')))
        df = df.loc[:, cols]
        # set Name col as index
        self.df = df.set_index('Name')
        # create csv
        self.df.to_csv(self.outfile)

    def __classify(self, df):
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

    def __add_index(self, df, idx):
        i = list(string.ascii_uppercase)[idx]
        cols = [ i+str(c+1) for c in df.index ]
        df.insert(loc=0, column='Name', value=cols)
        return df
