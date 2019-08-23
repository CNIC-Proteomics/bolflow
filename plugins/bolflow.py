import pandas
import re


__author__ = 'jmrodriguezc'


class bolflow:
    '''
    Make the calculations in the workflow
    '''
    def __init__(self, i, c):
        # init labels
        self.title_samples    = 'Samples'
        self.title_stype      = 'Sample Type'
        self.title_group      = 'Group'
        self.title_cohort     = 'Cohort'
        self.title_bat_cohort = 'Cohort Batch'
        self.title_max        = 'Max'
        self.lbl_qc           = 'QC'
        self.lbl_blank        = 'B'
        self.lbl_sample       = 'S'
        self.icol_name        = 'Name'
        self.incol_mz         = 'Apex m/z'
        self.incol_rt         = 'RT [min]'
        self.incol_max_area   = 'Max. Area'
        self.df = None
        # get data file
        if i:
            self.df = pandas.read_csv(i, na_values=['NA'], low_memory=False).set_index(self.icol_name)
            # get experiments
            self.exps = [name for name in self.df.index if re.search(r'^\w{1}\d+$', name)]
        # get classifycation data
        if c:
            df_c = pandas.read_excel(c, na_values=['NA'])
            # get groups ( discarding the 'QC' )
            g = df_c[self.title_group].dropna().unique()
            self.group = [ c for c in g if not self.lbl_qc in c and not self.lbl_blank in c ]
            # get the names of QC
            self.samples_qc = df_c.loc[df_c[self.title_group] == self.lbl_qc, self.title_samples].dropna().unique()
            # get the group-cohort
            cohort = sorted( df_c[self.title_cohort].dropna().unique().tolist() )
            cohort_batch = sorted( df_c[self.title_bat_cohort].dropna().unique().tolist() )
            if 0 in cohort_batch:
                cohort_batch.remove(0)
            self.group_cor = []
            for grp in self.group:
                for coh in cohort:
                    self.group_cor.append(str(grp)+'-'+str(coh))
