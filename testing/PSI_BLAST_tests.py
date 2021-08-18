import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class PSI_BLAST_tests(unittest.TestCase):
    """
    Runs all tests for the PSI_BLAST class.
    """   
    def test_execution(self):
        """
        Tests the ability of the PSI_BLAST_tests class to run a test.
        
        :param self: An instance of the PSI_BLAST_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()