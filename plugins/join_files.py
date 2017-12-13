import pandas
import string

__author__ = 'jmrodriguezc'


class joinFiles:
    '''
    Join the Metabolomic files into unique file
    '''
    def __init__(self, i, c, o):
        self.infiles = i
        self.inclass = c
        self.outfile = o
        self.df = None

    def join(self):
        dfs = []
        for idx, infile in enumerate(self.infiles):
            d = pandas.read_excel(infile, na_values=['NA'])
            # delete cols
            d = self.delete_cols(d)
            # create index
            d = self.add_index(d, idx)
            dfs.append(d)    
        # get classification file
        dfs.insert(0, self.classify())
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
        self.df.to_csv(self.outfile, sep="\t")

    def frequency(self):
        # create frequency df
        cols = ['Freq C','Freq D','Freq All','Freq QCs','Freq 2a C','Freq 2a D','Freq 3a C','Freq 3a D','Freq 4a C','Freq 4a D','Freq 5a C','Freq 5a D','Freq 2a QC','Freq 3a QC','Freq 4a QC','Freq 5a QC']
        d = pandas.DataFrame(index=self.df.index, columns=cols)
        d.index.name = 'Name'
        # freq. based on the groups
        icol = 3
        # for name in self.df.index:
        #     if name != 'Group':
        #         print("-- "+name)
        #         d = self.df.ix[('Group',name),icol:].transpose()
        #         c = d.groupby(['Group']).count().transpose()
        #         print(c)
        # freq. based on group-cohort
        for name in self.df.index:
            if name != 'Group' and name != 'Cohort':
                print("-- "+name)
                d = self.df.ix[('Group','Cohort',name),icol:].transpose()
                c = d.groupby(['Group','Cohort']).count().transpose()
                print(c)

    def classify(self):
        d = pandas.read_excel(self.inclass, na_values=['NA'])
        df = d.set_index('Samples').transpose()
        df.insert(loc=0, column='Name', value=df.index)
        df.index = range(len(df))
        return df

    def delete_cols(self, df):
        # header names that will be deleted
        cols = [ c for c in df.columns if '.raw' in c.lower() or c.lower() in ['checked','name','comments'] ]
        d = df.drop(cols, axis=1)
        # rename some headers
        d.columns = d.columns.str.replace('\s*Group Area:\s*', '')
        return d

    def add_index(self, df, idx):
        i = list(string.ascii_uppercase)[idx]
        cols = [ i+str(c+1) for c in df.index ]
        df.insert(loc=0, column='Name', value=cols)
        return df
