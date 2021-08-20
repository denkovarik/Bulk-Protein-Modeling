import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from classes.strategy import Outfmt_0_Strat


class Outfmt_0_Strat_tests(unittest.TestCase):
    """
    Runs all tests for the Outfmt_0_Strat class.
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
        itr = Outfmt_0_Strat(content, outfmt0_path)
        next(itr)
        self.assertTrue(itr.features['accession'] == '4JOM_A')
        self.assertTrue(itr.features['score'] == 231.0)
        self.assertTrue(itr.features['e_value'] == float("4e-68"))
        self.assertTrue(itr.features['per_ident'] == 40.0)
        next(itr)
        self.assertTrue(itr.features['accession'] == '2HNH_A')
        self.assertTrue(itr.features['score'] == 227.0)
        self.assertTrue(itr.features['e_value'] == float("1e-66"))
        self.assertTrue(itr.features['per_ident'] == 39.0)
        
        
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
        itr = Outfmt_0_Strat(content, outfmt0_path)
        
        
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
        itr = Outfmt_0_Strat(content, outfmt0_path)
        itr.start_pos = 0
        itr.begin()
        self.assertTrue(itr.start_pos == 1165)
        
        
    def test_is_outfmt_0(self):
        """
        Tests the Outfmt_0_Strat class member function is_outfmt0 
        on its ability to determine if a blast results file is in 
        the outfmt 0 format.
        
        :param self: An instance of the Outfmt_0_Strat_tests class.
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
        # Testing BLAST rslt outfmt 1
        outfmt0_path = currentdir + "\\test_files\\outfmt_1.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertFalse(Outfmt_0_Strat.is_outfmt_0(content, ext))
        # Testing BLAST rslt outfmt 2
        outfmt0_path = currentdir + "\\test_files\\outfmt_2.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertFalse(Outfmt_0_Strat.is_outfmt_0(content, ext))
        # Testing BLAST rslt outfmt 3
        outfmt0_path = currentdir + "\\test_files\\outfmt_3.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertFalse(Outfmt_0_Strat.is_outfmt_0(content, ext))
        # Testing BLAST rslt outfmt 4
        outfmt0_path = currentdir + "\\test_files\\outfmt_4.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertFalse(Outfmt_0_Strat.is_outfmt_0(content, ext))
        # Testing BLAST rslt outfmt 5
        outfmt0_path = currentdir + "\\test_files\\outfmt_5.xml"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "xml")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertFalse(Outfmt_0_Strat.is_outfmt_0(content, ext))
        # Testing BLAST rslt outfmt 0 with no matches
        outfmt0_path = currentdir + "\\test_files\\outfmt_0_no_matches.txt"
        os.path.isfile(outfmt0_path)
        ext = outfmt0_path.split(".")[-1]
        self.assertTrue(ext == "txt")
        # Read the file
        with open(outfmt0_path) as f:
            content = f.read()
        self.assertFalse(Outfmt_0_Strat.is_outfmt_0(content, ext))
        
        
    def test_execution(self):
        """
        Tests the ability of the Outfmt_0_Strat_tests class to run a test.
        
        :param self: An instance of the Outfmt_0_Strat_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()