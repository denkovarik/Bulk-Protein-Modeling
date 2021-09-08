from classes.strategy import *


class BLAST_Rslts_Itr():
    """
    Iterator for the results returned from BLAST
    """
    def __init__(self, content, filepath):
        """
        Initializes an instance of the BLAST_Rslts_Itr class.
        
        :param self: An instance of the BLAST_Rslts_Itr class
        :param content: The content of the BLAST Results
        :param filepath: The filepath to the BLAST rslts file.
        """
        self.strategy = None
        self.choose_strategy(content, filepath.split(".")[-1])
                    
            
    def __iter__(self):
        """
        The overload iter python built-in to make the class iterable.
        
        :param self: An instance of the BLAST_Rslts_Itr class.
        :return: An iterator for the BLAST results
        """
        return self
        
        
    def __next__(self):
        """
        Sets the instance of the BLAST_Rslts_Itr class to the next 
        result of all the results returned from BLAST.
            
        :param self: An instance of the BLAST_Rslts_Itr class
        :return: The extrated features of the row
        """
        if not self.strategy is None:
            return self.strategy.__next__()
        
        
    def choose_strategy(self, content, filepath):
        """
        Determines the strategy to use for the class.
        
        :param self: An instance of the BLAST_Rslts_Itr class
        :param content: The content to iterate overload
        :param ext: The extension of the file being iterated over
        """
        ext = filepath.split(".")[-1]
        if Outfmt_0_Strat.is_outfmt_0(content, ext):
            self.strategy = Outfmt_0_Strat(content, filepath)
        else:
            raise Exception("Unrecognized BLAST Results in " + filepath)
            
            
    def begin(self):
        """
        Sets the instance of the BLAST_Rslts_Itr class to the beginning of the
        results returned from BLAST.
            
        :param self: An instance of the BLAST_Rslts_Itr class
        """
        if not self.strategy is None:
            self.strategy.begin()
        
        
    def end_itr(self):
        """
        Marks the class as at the end of iteration.
        
        :param self: An instance of the BLAST_Rslts_Itr class.
        """
        if not self.strategy is None:
            self.strategy.end_itr()
        
        
    def extract_features(self, row):
        """
        Extracts the features from the 'row' parameter, which is a row from
        the results table from a BLAST query. The features that are 
        currently being extracted are the id and the protein names.
         
        :param self: An instance of the BLAST_Rslts_Itr class.
        :param row: A row from the results table in the html file as a String
        """
        if not self.strategy is None:
            self.strategy.end_itr()