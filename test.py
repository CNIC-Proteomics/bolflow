import unittest
import os,sys

# import components for bolflow
from plugins import join_files

class bolflowTests(unittest.TestCase):
    '''
    Battery tests for the 'bolflow' workflow
    '''
    def setUp(self):
        indir = os.path.dirname(os.path.abspath(__file__))+'/test'
        infiles = [
            indir+'/test1-in1.xlsx',
            indir+'/test1-in2.xlsx'
        ]
        inclass = indir+'/test1-inC.xlsx'
        outfile = indir+'/test1-out.tsv'
        self.widget = join_files.joinFiles(infiles, inclass, outfile)

    def testJoinFiles(self):
        self.widget.join()

    def testFrequency(self):
        self.widget.join()
        self.widget.frequency()

def main():
    unittest.main()

if __name__ == '__main__':
    main()