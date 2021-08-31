import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from classes.BLAST_Rslts_Itr import BLAST_Rslts_Itr
from classes.strategy import Outfmt_0_Strat


class BLAST_Rslts_Itr_tests(unittest.TestCase):
    """
    Runs all tests for the BLAST_Rslts_Itr class.
    """         
    def test_next(self):
        """
        Tests the overloaded python function next()
        """
        # Testing BLAST rslt outfmt 0
        outfmt0_path = currentdir + "\\test_files\\outfmt_0.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertTrue(Outfmt_0_Strat.is_outfmt_0(content, ext))
        itr = BLAST_Rslts_Itr(content, outfmt0_path)
        next(itr)
        self.assertTrue(itr.strategy.features['accession'] == '4JOM_A')
        self.assertTrue(itr.strategy.features['score'] == 231.0)
        self.assertTrue(itr.strategy.features['e_value'] == float("4e-68"))
        self.assertTrue(itr.strategy.features['per_ident'] == 40.0)
        next(itr)
        self.assertTrue(itr.strategy.features['accession'] == '2HNH_A')
        self.assertTrue(itr.strategy.features['score'] == 227.0)
        self.assertTrue(itr.strategy.features['e_value'] == float("1e-66"))
        self.assertTrue(itr.strategy.features['per_ident'] == 39.0)
        
        #for features in iter(BLAST_Rslts_Itr(content, outfmt0_path)):
        #    print(features)
        
        
    def test_init(self):
        """
        Tests the Outfmt_0_Strat class member function init
        """
        # Testing BLAST rslt outfmt 0
        outfmt0_path = currentdir + "\\test_files\\outfmt_0.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertTrue(Outfmt_0_Strat.is_outfmt_0(content, ext))
        itr = BLAST_Rslts_Itr(content, outfmt0_path)
        
        
    def test_begin(self):
        """
        Tests the Outfmt_0_Strat class member function begin
        """
        # Testing BLAST rslt outfmt 0
        outfmt0_path = currentdir + "\\test_files\\outfmt_0.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertTrue(Outfmt_0_Strat.is_outfmt_0(content, ext))
        itr = BLAST_Rslts_Itr(content, outfmt0_path)
        itr.strategy.start_pos = 0
        itr.strategy.begin()
        self.assertTrue(itr.strategy.start_pos == 1165)
    
    
    def test_execution(self):
        """
        Tests the ability of the BLAST_Rslts_Itr_tests class to run a test.
        
        :param self: An instance of the BLAST_Rslts_Itr_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()