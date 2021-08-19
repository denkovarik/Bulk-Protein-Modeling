import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
#from classes.BLAST_Rslts_Itr import BLAST_Rslts_Itr


class BLAST_Rslts_Itr_tests(unittest.TestCase):
    """
    Runs all tests for the BLAST_Rslts_Itr class.
    """         
    def test_execution(self):
        """
        Tests the ability of the BLAST_Rslts_Itr_tests class to run a test.
        
        :param self: An instance of the BLAST_Rslts_Itr_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()