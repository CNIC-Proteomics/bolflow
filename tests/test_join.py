import unittest
import os,sys

# import components for bolflow
from plugins import predata

class bolflowTests(unittest.TestCase):
    '''
    Battery tests for the 'bolflow' workflow
    '''
    def setUp(self):
        indir = os.path.dirname(os.path.abspath(__file__))
        infiles = [
            indir+'/test1-in1.xlsx',
            indir+'/test1-in2.xlsx'
        ]
        inclass = indir+'/test1-inC.xlsx'
        outfile = indir+'/test1-out.csv'
        self.widget = predata.preData(infiles, inclass, outfile)

    def testJoinFiles(self):
        self.widget.join()
    
    # testCV (Coefficient of Variation)

    # testFilters (filters of frequency)

    # testNormaCV (normalization of CV's)

    # testDiscardDuplicates

     

def main():
    unittest.main()

if __name__ == '__main__':
    main()