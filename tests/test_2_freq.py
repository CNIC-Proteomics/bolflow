import unittest
import os,sys

# import components for bolflow
from plugins import calc

class bolflowTests(unittest.TestCase):
    '''
    Battery tests for the 'bolflow' workflow
    '''
    def setUp(self):
        indir = os.path.dirname(os.path.abspath(__file__))
        infile = indir+'/test1-out.join.csv'
        outfile = indir+'/test1-out.freq.csv'
        self.widget = calc.calculate(infile, outfile)

    def testFrequency(self):
        self.widget.frequency()
    
    # testCV (Coefficient of Variation)

    # testFilters (filters of frequency)

    # testNormaCV (normalization of CV's)

    # testDiscardDuplicates

     

def main():
    unittest.main()

if __name__ == '__main__':
    main()