import pandas
import string

__author__ = 'jmrodriguezc'


class calculate:
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i, o):
        self.infile = i
        self.outfile = o
        self.df = pandas.read_csv(self.infile, na_values=['NA']).set_index('Name')
        self.group_lbl = 'Group'
        g = self.df.loc[self.group_lbl].dropna().unique()
        self.qc_lbl = 'QC'
        self.group = [ c for c in g if not self.qc_lbl in c ] # discard 'QC'

    def frequency(self):
        '''
        Calculate the frequency
        '''
        # freq. based on the groups
        # icol = 3
#         df1s = []
#         for name in self.df.index:
#             if name != 'Group':
#                 d = self.df.ix[('Group',name),icol:].transpose()
#                 c = d.groupby(['Group']).count().transpose()
#                 df1s.append(c)
#             # for the same name, we have to duplicate column and rename
# # BAD!!!
# # TODO!! good!! talk with Alessia
#             elif name == 'Group':
#                 d = self.df.ix[('Group',name),icol:].transpose()
#                 d.columns = ['Group_0','Group']
#                 c = d.groupby(['Group_0']).count().transpose()               
#                 df1s.append(c)
#         df1 = pandas.concat(df1s)
#         # add frequency ALL into the prelast position (discarding QC)
#         cols = [ c for c in df1.columns if not 'QC' in c ]
#         df1.insert(loc= len(df1.columns)-1, column='ALL', value=df1[cols].sum(axis=1))

        # freq. based on group-cohort
#         df2s = []
#         for name in self.df.index:
#             if name != 'Group' and name != 'Cohort':
#                 d = self.df.loc[['Group','Cohort',name]].iloc[:,icol:].transpose()
#                 # apply threshold
#                 if name == 'Cohort ORDER':
#                     d = d[d[name].astype(int) > 30]
#                 elif name == 'Cohort Batch':
#                     d = d[d[name].astype(int) > 1]
#                 c = d.groupby(['Group','Cohort']).count().transpose()
#                 df2s.append(c)
#             # for the same name, we have to duplicate column and rename
# # TODO!! good!! talk with Alessia
#             # elif name == 'Group':
#             #     d = self.df.loc[['Group','Cohort',name]].iloc[:,icol:].transpose()
#             #     d.columns = ['Group_0','Cohort','Group']
#             #     c = d.groupby(['Group_0','Cohort']).count().transpose()
#             #     df2s.append(c)
#             # for the same name, we have to duplicate column and rename
#             elif name == 'Cohort':
#                 d = self.df.loc[['Group','Cohort',name]].iloc[:,icol:].transpose()
#                 d.columns = ['Group','Cohort_0','Cohort']
#                 c = d.groupby(['Group','Cohort_0']).count().transpose()
#                 df2s.append(c)
#         df2 = pandas.concat(df2s)
#         # convert multiple index column ('Group','Cohort') in unique index
#         df2.columns = ['-'.join(col).strip() for col in df2.columns.values]

        # freq. based on the groups
        df1 = self.__freq_a(['Group'], True)
        print(df1)

        # freq. based on per single batch
        df1_1 = self.__freq_s(df1,'Group')
        print(df1_1)

        # freq. based on group-cohort
        df2 = self.__freq_a(['Group','Cohort'])
        print(df2)

        # freq. based on per single batch
        # df2_1 = self.__freq_s2(df2,'Group',['B','C','D'])
        # print(df2_1)

        # df2_1 = self.__freq_s2(df2,'Cohort Batch',['B','C','D'])
        # print(df2_1)
        
        # # concat freq's and print
        # df = pandas.concat([df1,df2,df1_1,df2_1], axis=1, join_axes=[self.df.index])
        # df.columns = ['Freq_' + col for col in df.columns.values]
        # self.df = pandas.concat([df,self.df], axis=1)
        # self.df.to_csv(self.outfile)

    def __freq_a(self,grp,all=False):
        icol = 3
        dfs = []
        for name in self.df.index:
            # extract the 'grp' columns and the actual 'name'
            g = grp[:]
            g.append(name)
            if not name in grp:
                d = self.df.loc[g].iloc[:,icol:].transpose()
                # print('-- '+name)
                # print(d)
# TODO!! good!! talk with Alessia
                # # apply threshold
                # if name == 'Cohort ORDER':
                #     d = d[d[name].astype(int) > 30]
                # elif name == 'Cohort Batch':
                #     d = d[d[name].astype(int) > 1]
                # group by 'grp' and count the frequency
                c = d.groupby(grp).count().transpose()
                dfs.append(c)
# TODO!! good!! talk with Alessia
            # for the same name, we have to duplicate column and rename
            elif name in grp:
                d = self.df.loc[g].iloc[:,icol:].transpose()
                name_0 = name+'_0'
                d.columns.values[-1] = name_0
                c = d.groupby(grp).count().transpose()
                c = c.rename(index={name_0: name})
                dfs.append(c)
        df = pandas.concat(dfs)
        if all:
            df.insert(loc=0, column='ALL', value=df[self.group].sum(axis=1))
        # # convert multiple index column ('Group','Cohort') in unique index
        # df.columns = ['-'.join(col).strip() for col in df.columns.values]
        return df

    def __freq_s(self,df,cmp):
        n = ['ALL','QC']
        c = ['byFALL','byFQC']
        group = df.loc[cmp,n]
        df_1 = pandas.DataFrame(index=self.df.index, columns=n)
        for name,row in df.iterrows():
            if not ('Group' in name) and not ('Cohort' in name) and not ('Global' in name):
                d = df.loc[name,n]
                df_1.loc[name] = (d >= group)
        df_1.columns = c
        return df_1


    def __freq_s2(self,df,cmp,ns):
        print(df)
        # a = [i for i in ns if i in df.columns]
        a = [x for x in df.columns if any(y in x for y in ns)]
        print(a)
        # n = ['ALL','QC']
        # c = ['byFALL','byFQC']
        # group = df.loc['Group',n]
        # df_1 = pandas.DataFrame(index=self.df.index, columns=n)
        # # df2_1 = pandas.DataFrame(index=self.df.index, columns=['byFGroup','byFCohort','byFGroupQC'])

        # for name,row in df.iterrows():
        #     if not ('Group' in name) and not ('Cohort' in name) and not ('Global' in name):
        #         d = df.loc[name,n]
        #         df_1.loc[name] = (d >= group)
        # df_1.columns = c
        # return df_1



