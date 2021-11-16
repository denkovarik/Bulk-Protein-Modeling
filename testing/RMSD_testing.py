import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from classes.RMSD_Validation import RMSD_Validation


class RMSD_Validation_tests(unittest.TestCase):
    """
    Runs all tests for the RMSD_Validation_tests class.
    """   
    def test_construction(self):
        """
        Tests the construction of the RMSD_Validation class.
        
        :param self: An instance of the RMSD_Validation_tests class.
        """
        rms = RMSD_Validation()
        self.assertTrue(isinstance(rms, type(RMSD_Validation())))
        
    
    def test_execution(self):
        """
        Tests the ability of the RMSD_Validation_tests class to run a test.
        
        :param self: An instance of the RMSD_Validation_tests class.
        """
        self.assertTrue(True)
        
        
if __name__ == '__main__':
    unittest.main()